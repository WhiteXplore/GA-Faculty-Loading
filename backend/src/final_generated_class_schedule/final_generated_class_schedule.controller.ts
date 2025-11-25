import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
} from '@nestjs/common';
import { FinalGeneratedClassScheduleService } from './final_generated_class_schedule.service';
import { CreateFinalGeneratedClassScheduleDto } from './dto/create-final_generated_class_schedule.dto';
import { UpdateFinalGeneratedClassScheduleDto } from './dto/update-final_generated_class_schedule.dto';

@Controller('final-generated-class-schedule')
export class FinalGeneratedClassScheduleController {
  constructor(private readonly service: FinalGeneratedClassScheduleService) {}

  // Single schedule
  @Post()
  create(@Body() createDto: CreateFinalGeneratedClassScheduleDto) {
    return this.service.create(createDto);
  }

  // Bulk schedules
  @Post('bulk')
  createMany(@Body() createDtos: CreateFinalGeneratedClassScheduleDto[]) {
    return this.service.createMany(createDtos);
  }

  @Get('get-all-final-schedules')
  findAll() {
    return this.service.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.service.findOne(+id);
  }

  @Patch(':id')
  update(
    @Param('id') id: string,
    @Body() updateDto: UpdateFinalGeneratedClassScheduleDto,
  ) {
    return this.service.update(+id, updateDto);
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.service.remove(+id);
  }
}
