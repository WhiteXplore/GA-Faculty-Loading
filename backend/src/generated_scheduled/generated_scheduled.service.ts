import { Injectable } from '@nestjs/common';
import { CreateGeneratedScheduledDto } from './dto/create-generated_scheduled.dto';
import { UpdateGeneratedScheduledDto } from './dto/update-generated_scheduled.dto';

@Injectable()
export class GeneratedScheduledService {
  create(createGeneratedScheduledDto: CreateGeneratedScheduledDto) {
    return 'This action adds a new generatedScheduled';
  }

  findAll() {
    return `This action returns all generatedScheduled`;
  }

  findOne(id: number) {
    return `This action returns a #${id} generatedScheduled`;
  }

  update(id: number, updateGeneratedScheduledDto: UpdateGeneratedScheduledDto) {
    return `This action updates a #${id} generatedScheduled`;
  }

  remove(id: number) {
    return `This action removes a #${id} generatedScheduled`;
  }
}
