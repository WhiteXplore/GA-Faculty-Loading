import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { UnscheduledMeeting } from './entities/unscheduled_meeting.entity';
import { CreateUnscheduledMeetingDto } from './dto/create-unscheduled_meeting.dto';
import { UpdateUnscheduledMeetingDto } from './dto/update-unscheduled_meeting.dto';

@Injectable()
export class UnscheduledMeetingsService {
  constructor(
    @InjectRepository(UnscheduledMeeting)
    private readonly repository: Repository<UnscheduledMeeting>,
  ) {}

  async create(data: CreateUnscheduledMeetingDto[]) {
    if (!data || !data.length) return [];

    const meetings = this.repository.create(data);
    return await this.repository.save(meetings);
  }

  async findAll() {
    return await this.repository.find({
      order: { created_at: 'DESC' },
    });
  }

  async findOne(id: number) {
    return await this.repository.findOne({ where: { id } });
  }

  async update(id: number, updateDto: UpdateUnscheduledMeetingDto) {
    await this.repository.update(id, updateDto);
    return this.findOne(id);
  }

  async remove(id: number) {
    return await this.repository.delete(id);
  }
}
