import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { FinalGeneratedClassSchedule } from './entities/final_generated_class_schedule.entity';
import { CreateFinalGeneratedClassScheduleDto } from './dto/create-final_generated_class_schedule.dto';
import { UpdateFinalGeneratedClassScheduleDto } from './dto/update-final_generated_class_schedule.dto';

@Injectable()
export class FinalGeneratedClassScheduleService {
  constructor(
    @InjectRepository(FinalGeneratedClassSchedule)
    private readonly scheduleRepo: Repository<FinalGeneratedClassSchedule>,
  ) {}

  // Save a single schedule
  async create(createDto: CreateFinalGeneratedClassScheduleDto) {
    const schedule = this.scheduleRepo.create(createDto);
    return await this.scheduleRepo.save(schedule);
  }

  // Save multiple schedules at once
  async createMany(createDtos: CreateFinalGeneratedClassScheduleDto[]) {
    const schedules = this.scheduleRepo.create(createDtos);
    return await this.scheduleRepo.save(schedules);
  }

  findAll() {
    return this.scheduleRepo.find();
  }

  findOne(id: number) {
    return this.scheduleRepo.findOneBy({ id });
  }

  async update(id: number, updateDto: UpdateFinalGeneratedClassScheduleDto) {
    await this.scheduleRepo.update(id, updateDto);
    return this.findOne(id);
  }

  async remove(id: number) {
    const schedule = await this.findOne(id);
    if (!schedule) {
      throw new Error(`Schedule with ID ${id} not found`);
    }
    return this.scheduleRepo.remove(schedule);
  }
}
