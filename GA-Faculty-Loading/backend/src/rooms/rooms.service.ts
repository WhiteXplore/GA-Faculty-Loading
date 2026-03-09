import {
  Injectable,
  NotFoundException,
  BadRequestException,
} from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';

import { Room } from './entities/room.entity';
import { CreateRoomDto } from './dto/create-room.dto';
import { UpdateRoomDto } from './dto/update-room.dto';

import { Institute } from 'src/institute/entities/institute.entity';
import { Building } from 'src/buildings/entities/building.entity';

@Injectable()
export class RoomsService {
  constructor(
    @InjectRepository(Room)
    private readonly roomRepository: Repository<Room>,

    @InjectRepository(Institute)
    private readonly instituteRepository: Repository<Institute>,

    @InjectRepository(Building)
    private readonly buildingRepository: Repository<Building>,
  ) {}

  // CREATE ROOM
  async create(createRoomDto: CreateRoomDto) {
    const room = new Room();

    room.room_name = createRoomDto.room_name;
    room.room_capacity = createRoomDto.room_capacity;
    room.room_type = createRoomDto.room_type;

    // attach institute
    if (createRoomDto.institute_id) {
      const institute = await this.instituteRepository.findOne({
        where: { institute_id: createRoomDto.institute_id },
      });

      if (!institute) {
        throw new BadRequestException('Institute not found');
      }

      room.institute = institute;
    }

    // attach building
    if (createRoomDto.building_id) {
      const building = await this.buildingRepository.findOne({
        where: { building_id: createRoomDto.building_id },
      });

      if (!building) {
        throw new BadRequestException('Building not found');
      }

      room.building = building;
    }

    return await this.roomRepository.save(room);
  }

  // GET ALL ROOMS
  async findAll() {
    return await this.roomRepository.find({
      relations: [
        'institute',
        'building',
        'building.buildingArea',
        'building.buildingArea.collegeBranch',
      ],
    });
  }

  // GET SINGLE ROOM
  async findOne(id: number) {
    const room = await this.roomRepository.findOne({
      where: { room_id: id },
      relations: [
        'institute',
        'building',
        'building.buildingArea',
        'building.buildingArea.collegeBranch',
      ],
    });

    if (!room) {
      throw new NotFoundException(`Room with ID ${id} not found`);
    }

    return room;
  }

  // UPDATE ROOM
  async update(id: number, updateRoomDto: UpdateRoomDto) {
    const room = await this.findOne(id);

    room.room_name = updateRoomDto.room_name ?? room.room_name;
    room.room_capacity = updateRoomDto.room_capacity ?? room.room_capacity;
    room.room_type = updateRoomDto.room_type ?? room.room_type;

    // update institute
    if (updateRoomDto.institute_id !== undefined) {
      if (updateRoomDto.institute_id === null) {
        room.institute = null;
      } else {
        const institute = await this.instituteRepository.findOne({
          where: { institute_id: updateRoomDto.institute_id },
        });

        if (!institute) {
          throw new BadRequestException('Institute not found');
        }

        room.institute = institute;
      }
    }

    // update building
    if (updateRoomDto.building_id !== undefined) {
      if (updateRoomDto.building_id === null) {
        room.building = null;
      } else {
        const building = await this.buildingRepository.findOne({
          where: { building_id: updateRoomDto.building_id },
        });

        if (!building) {
          throw new BadRequestException('Building not found');
        }

        room.building = building;
      }
    }

    return await this.roomRepository.save(room);
  }

  // DELETE ROOM
  async remove(id: number) {
    const room = await this.findOne(id);
    return await this.roomRepository.remove(room);
  }
}
