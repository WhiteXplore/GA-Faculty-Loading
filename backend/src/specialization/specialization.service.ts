import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Specialization } from './entities/specialization.entity';
import { CreateSpecializationDto } from './dto/create-specialization.dto';
import { UpdateSpecializationDto } from './dto/update-specialization.dto';

@Injectable()
export class SpecializationService {
  constructor(
    @InjectRepository(Specialization)
    private readonly specializationRepository: Repository<Specialization>,
  ) {}

  async create(
    createSpecializationDto: CreateSpecializationDto,
  ): Promise<Specialization> {
    const specialization = this.specializationRepository.create(
      createSpecializationDto,
    );
    return await this.specializationRepository.save(specialization);
  }

  async findAll(): Promise<Specialization[]> {
    return await this.specializationRepository.find({
      relations: ['program', 'program.institute'],
      order: { created_at: 'DESC' },
    });
  }

  async findOne(id: number): Promise<Specialization> {
    const specialization = await this.specializationRepository.findOne({
      where: { specialization_id: id },
      relations: ['program', 'program.institute'],
    });
    if (!specialization) {
      throw new NotFoundException(`Specialization with ID ${id} not found`);
    }
    return specialization;
  }

  async update(
    id: number,
    updateSpecializationDto: UpdateSpecializationDto,
  ): Promise<Specialization> {
    const specialization = await this.specializationRepository.preload({
      specialization_id: id,
      ...updateSpecializationDto,
    });
    if (!specialization) {
      throw new NotFoundException(`Specialization with ID ${id} not found`);
    }
    return await this.specializationRepository.save(specialization);
  }

  async remove(id: number): Promise<void> {
    const specialization = await this.findOne(id);
    await this.specializationRepository.remove(specialization);
  }
}

