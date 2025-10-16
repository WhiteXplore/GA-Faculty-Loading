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
    const schoolYear = this.schoolYearRepository.create(createSchoolYearDto);
    return await this.schoolYearRepository.save(schoolYear);
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

