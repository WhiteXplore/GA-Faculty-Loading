import { Injectable, NotFoundException, BadRequestException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Room } from './entities/room.entity';
import { CreateRoomDto } from './dto/create-room.dto';
import { UpdateRoomDto } from './dto/update-room.dto';
import { Institute } from 'src/institute/entities/institute.entity';
import * as XLSX from 'xlsx';

@Injectable()
export class RoomsService {
  constructor(
    @InjectRepository(Room)
    private readonly roomRepository: Repository<Room>,
    @InjectRepository(Institute)
    private readonly instituteRepository: Repository<Institute>,
  ) {}

  async create(createRoomDto: CreateRoomDto) {
    const room = this.roomRepository.create(createRoomDto);
    return await this.roomRepository.save(room);
  }

  async findAll() {
    return await this.roomRepository.find({
      relations: ['institute'],
    });
  }

  async findOne(id: number) {
    const room = await this.roomRepository.findOne({ where: { room_id: id } });
    if (!room) {
      throw new NotFoundException(`Room with ID ${id} not found`);
    }
    return room;
  }

  async update(id: number, updateRoomDto: UpdateRoomDto) {
    const room = await this.findOne(id); // Ensure it exists
    const updatedRoom = Object.assign(room, updateRoomDto);
    return await this.roomRepository.save(updatedRoom);
  }

  async remove(id: number) {
    const room = await this.findOne(id);
    return await this.roomRepository.remove(room);
  }

  async uploadExcel(file: any) {
    if (!file) {
      throw new BadRequestException('No file uploaded');
    }

    // Check file type
    const allowedTypes = [
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      'application/vnd.ms-excel',
    ];
    if (!allowedTypes.includes(file.mimetype)) {
      throw new BadRequestException('Only Excel files (.xlsx, .xls) are allowed');
    }

    try {
      // Parse Excel file
      const workbook = XLSX.read(file.buffer, { type: 'buffer' });
      const sheetName = workbook.SheetNames[0];
      const worksheet = workbook.Sheets[sheetName];
      const jsonData = XLSX.utils.sheet_to_json(worksheet);

      if (!jsonData || jsonData.length === 0) {
        throw new BadRequestException('Excel file is empty');
      }

      // Get all institutes to map names to IDs
      const institutes = await this.instituteRepository.find();
      const instituteMap = new Map<string, number>();
      institutes.forEach(inst => {
        instituteMap.set(inst.institute_code.toUpperCase(), inst.institute_id);
        instituteMap.set(inst.institute_name.toUpperCase(), inst.institute_id);
      });

      const roomsToCreate: CreateRoomDto[] = [];
      const errors: string[] = [];

      // Process each row
      for (let i = 0; i < jsonData.length; i++) {
        const row: any = jsonData[i];
        const rowNumber = i + 2; // Excel row number (accounting for header)

        try {
          // Extract data from row (handle various column name formats)
          const roomName = row['Room Name'] || row['room_name'] || row['RoomName'] || row['ROOM NAME'];
          const roomCapacity = row['Room Capacity'] || row['room_capacity'] || row['RoomCapacity'] || row['ROOM CAPACITY'];
          const roomType = row['Room Type'] || row['room_type'] || row['RoomType'] || row['ROOM TYPE'];
          const instituteName = row['Institute'] || row['institute'] || row['INSTITUTE'];

          // Validate required fields
          if (!roomName) {
            errors.push(`Row ${rowNumber}: Room Name is required`);
            continue;
          }
          if (!roomCapacity) {
            errors.push(`Row ${rowNumber}: Room Capacity is required`);
            continue;
          }
          if (!roomType) {
            errors.push(`Row ${rowNumber}: Room Type is required`);
            continue;
          }

          // Find institute ID
          let instituteId: number | undefined;
          if (instituteName) {
            const instituteKey = String(instituteName).toUpperCase().trim();
            instituteId = instituteMap.get(instituteKey);
            if (!instituteId) {
              errors.push(`Row ${rowNumber}: Institute "${instituteName}" not found`);
            }
          }

          // Create room DTO
          const roomDto: CreateRoomDto = {
            room_name: String(roomName).trim(),
            room_capacity: Number(roomCapacity),
            room_type: String(roomType).trim(),
            institute_id: instituteId,
          };

          roomsToCreate.push(roomDto);
        } catch (error) {
          errors.push(`Row ${rowNumber}: ${error.message}`);
        }
      }

      // Save all rooms
      const savedRooms = await this.roomRepository.save(roomsToCreate);

      return {
        success: true,
        message: `Successfully imported ${savedRooms.length} rooms`,
        imported: savedRooms.length,
        total: jsonData.length,
        errors: errors.length > 0 ? errors : undefined,
      };
    } catch (error) {
      throw new BadRequestException(`Failed to process Excel file: ${error.message}`);
    }
  }
}
