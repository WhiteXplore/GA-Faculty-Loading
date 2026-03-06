import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Institute } from './entities/institute.entity';
import { CreateInstituteDto } from './dto/create-institute.dto';
import { UpdateInstituteDto } from './dto/update-institute.dto';

@Injectable()
export class InstituteService {
  constructor(
    @InjectRepository(Institute)
    private readonly instituteRepository: Repository<Institute>,
  ) {}

  async create(createInstituteDto: CreateInstituteDto): Promise<Institute> {
    const existing = await this.instituteRepository.findOne({
      where: { institute_code: createInstituteDto.institute_code },
    });

    // If institute already exists, return it instead of creating new
    if (existing) {
      return existing;
    }

    const institute = this.instituteRepository.create(createInstituteDto);
    return await this.instituteRepository.save(institute);
  }

  async findAll(): Promise<Institute[]> {
    return await this.instituteRepository.find();
  }

  async findOne(id: number): Promise<Institute> {
    const institute = await this.instituteRepository.findOneBy({
      institute_id: id,
    });
    if (!institute) {
      throw new NotFoundException(`Institute with ID ${id} not found`);
    }
    return institute;
  }

  async update(
    id: number,
    updateInstituteDto: UpdateInstituteDto,
  ): Promise<Institute> {
    const institute = await this.findOne(id);
    Object.assign(institute, updateInstituteDto);
    return await this.instituteRepository.save(institute);
  }

  async remove(id: number): Promise<void> {
    const institute = await this.findOne(id);
    await this.instituteRepository.remove(institute);
  }
}
