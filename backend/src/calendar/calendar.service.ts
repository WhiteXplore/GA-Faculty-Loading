import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Calendar } from './entities/calendar.entity';
import { CreateCalendarDto } from './dto/create-calendar.dto';
import { UpdateCalendarDto } from './dto/update-calendar.dto';

@Injectable()
export class CalendarService {
  constructor(
    @InjectRepository(Calendar)
    private readonly calendarRepository: Repository<Calendar>,
  ) {}

  async create(createCalendarDto: CreateCalendarDto): Promise<Calendar> {
    const newEvent = this.calendarRepository.create(createCalendarDto);
    return await this.calendarRepository.save(newEvent);
  }

  async findAll(): Promise<Calendar[]> {
    return await this.calendarRepository.find({
      relations: ['program', 'program.institute'],
    });
  }

  async findOne(id: number): Promise<Calendar> {
    const event = await this.calendarRepository.findOneBy({ id });
    if (!event) {
      throw new NotFoundException(`Calendar event #${id} not found`);
    }
    return event;
  }

  async update(
    id: number,
    updateCalendarDto: UpdateCalendarDto,
  ): Promise<Calendar> {
    const event = await this.findOne(id);
    const updated = Object.assign(event, updateCalendarDto);
    return await this.calendarRepository.save(updated);
  }

  async remove(id: number): Promise<void> {
    const event = await this.findOne(id);
    await this.calendarRepository.remove(event);
  }
}
