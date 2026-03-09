import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { SchoolYear } from './entities/school_year.entity';
import { CreateSchoolYearDto } from './dto/create-school_year.dto';
import { UpdateSchoolYearDto } from './dto/update-school_year.dto';

@Injectable()
export class SchoolYearService {
  constructor(
    @InjectRepository(SchoolYear)
    private readonly schoolYearRepository: Repository<SchoolYear>,
  ) {}

  async create(createSchoolYearDto: CreateSchoolYearDto): Promise<SchoolYear> {
    const exists = await this.schoolYearRepository.findOne({
      where: {
        school_year_name: createSchoolYearDto.school_year_name,
        semester: createSchoolYearDto.semester,
      },
    });

    if (exists) {
      throw new Error(
        `School year ${createSchoolYearDto.school_year_name} for semester ${createSchoolYearDto.semester} already exists`,
      );
    }

    const schoolYear = this.schoolYearRepository.create(createSchoolYearDto);
    return await this.schoolYearRepository.save(schoolYear);
  }

  async updateTimestamp(id: number) {
    // 1️⃣ Find the school year
    const year = await this.schoolYearRepository.findOne({
      where: { school_year_id: id },
    });

    if (!year) {
      return { message: '❌ School year not found' };
    }

    // 2️⃣ Update its timestamp (always, even if active)
    year.updated_at = new Date();
    await this.schoolYearRepository.save(year);

    return {
      message: '✅ School year timestamp updated successfully',
      data: year,
    };
  }

  // school_year.service.ts
  async findLatestActive(): Promise<SchoolYear> {
    const latestActiveYear = await this.schoolYearRepository.findOne({
      where: { is_active: true },
      order: { updated_at: 'DESC' },
    });

    if (!latestActiveYear) {
      throw new NotFoundException('No active school year found');
    }

    return latestActiveYear;
  }

  async findAll(): Promise<SchoolYear[]> {
    return await this.schoolYearRepository.find({
      order: { start_year: 'DESC' },
    });
  }

  async findOne(id: number): Promise<SchoolYear> {
    const schoolYear = await this.schoolYearRepository.findOne({
      where: { school_year_id: id },
    });
    if (!schoolYear) {
      throw new NotFoundException(`School Year with ID ${id} not found`);
    }
    return schoolYear;
  }

  async update(
    id: number,
    updateSchoolYearDto: UpdateSchoolYearDto,
  ): Promise<SchoolYear> {
    const schoolYear = await this.schoolYearRepository.preload({
      school_year_id: id,
      ...updateSchoolYearDto,
    });
    if (!schoolYear) {
      throw new NotFoundException(`School Year with ID ${id} not found`);
    }
    return await this.schoolYearRepository.save(schoolYear);
  }

  async remove(id: number): Promise<void> {
    const schoolYear = await this.findOne(id);
    await this.schoolYearRepository.remove(schoolYear);
  }
}
