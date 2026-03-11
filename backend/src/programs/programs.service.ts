import {
  Injectable,
  NotFoundException,
  BadRequestException,
} from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Program } from './entities/program.entity';
import { CreateProgramDto } from './dto/create-program.dto';
import { UpdateProgramDto } from './dto/update-program.dto';
import { Institute } from 'src/institute/entities/institute.entity';
import * as XLSX from 'xlsx';

@Injectable()
export class ProgramsService {
  constructor(
    @InjectRepository(Program)
    private readonly programRepository: Repository<Program>,
    @InjectRepository(Institute)
    private readonly instituteRepository: Repository<Institute>,
  ) {}

  async create(createProgramDto: CreateProgramDto): Promise<Program> {
    const existing = await this.programRepository.findOne({
      where: {
        program_code: createProgramDto.program_code,
        institute_id: createProgramDto.institute_id,
      },
    });

    if (existing) {
      return existing;
    }

    const newProgram = this.programRepository.create(createProgramDto);
    return await this.programRepository.save(newProgram);
  }

  async findAll(): Promise<Program[]> {
    return await this.programRepository.find({
      relations: ['institute'],
    });
  }

  async findOne(id: number): Promise<Program> {
    const program = await this.programRepository.findOne({
      where: { program_id: id },
      relations: ['institute'],
    });

    if (!program) {
      throw new NotFoundException(`Program with ID ${id} not found`);
    }

    return program;
  }

  async update(
    id: number,
    updateProgramDto: UpdateProgramDto,
  ): Promise<Program> {
    const program = await this.findOne(id);
    const updated = Object.assign(program, updateProgramDto);
    return await this.programRepository.save(updated);
  }

  async remove(id: number): Promise<void> {
    const program = await this.findOne(id);
    await this.programRepository.remove(program);
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
      throw new BadRequestException(
        'Only Excel files (.xlsx, .xls) are allowed',
      );
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
      institutes.forEach((inst) => {
        instituteMap.set(inst.institute_code.toUpperCase(), inst.institute_id);
        instituteMap.set(inst.institute_name.toUpperCase(), inst.institute_id);
      });

      // Get all existing programs to check for duplicates
      const existingPrograms = await this.programRepository.find();
      const existingProgramCodes = new Set(
        existingPrograms.map((p) => p.program_code.toUpperCase()),
      );

      const programsToCreate: CreateProgramDto[] = [];
      const errors: string[] = [];
      const skipped: string[] = [];

      // Process each row
      for (let i = 0; i < jsonData.length; i++) {
        const row: any = jsonData[i];
        const rowNumber = i + 2; // Excel row number (accounting for header)

        try {
          // Extract data from row (handle various column name formats)
          const instituteName =
            row['Institute'] || row['institute'] || row['INSTITUTE'];
          const programCode =
            row['Program'] ||
            row['program'] ||
            row['PROGRAM'] ||
            row['program_code'] ||
            row['Program Code'];
          const programName =
            row['Program Name'] ||
            row['program_name'] ||
            row['ProgramName'] ||
            row['PROGRAM NAME'];

          // Validate required fields
          if (!programCode) {
            errors.push(`Row ${rowNumber}: Program code is required`);
            continue;
          }
          if (!programName) {
            errors.push(`Row ${rowNumber}: Program name is required`);
            continue;
          }

          // Check for duplicates
          const programCodeUpper = String(programCode).toUpperCase().trim();
          if (existingProgramCodes.has(programCodeUpper)) {
            skipped.push(
              `Row ${rowNumber}: Program "${programCode}" already exists`,
            );
            continue;
          }

          // Find institute ID
          let instituteId: number | undefined;
          if (instituteName) {
            const instituteKey = String(instituteName).toUpperCase().trim();
            instituteId = instituteMap.get(instituteKey);
            if (!instituteId) {
              errors.push(
                `Row ${rowNumber}: Institute "${instituteName}" not found`,
              );
              continue;
            }
          }

          // Create program DTO
          const programDto: CreateProgramDto = {
            program_name: String(programName).trim(),
            program_code: String(programCode).trim(),
            institute_id: instituteId,
          };

          programsToCreate.push(programDto);
          // Add to existing set to prevent duplicates within the same file
          existingProgramCodes.add(programCodeUpper);
        } catch (error) {
          errors.push(`Row ${rowNumber}: ${error.message}`);
        }
      }

      // Save all programs
      const savedPrograms = await this.programRepository.save(programsToCreate);

      return {
        success: true,
        message: `Successfully imported ${savedPrograms.length} programs`,
        imported: savedPrograms.length,
        total: jsonData.length,
        skipped: skipped.length,
        errors: errors.length > 0 ? errors : undefined,
        skippedDetails: skipped.length > 0 ? skipped : undefined,
      };
    } catch (error) {
      throw new BadRequestException(
        `Failed to process Excel file: ${error.message}`,
      );
    }
  }
}
