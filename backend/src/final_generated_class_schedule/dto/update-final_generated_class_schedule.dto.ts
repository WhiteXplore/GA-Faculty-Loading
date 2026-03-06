import { PartialType } from '@nestjs/mapped-types';
import { CreateFinalGeneratedClassScheduleDto } from './create-final_generated_class_schedule.dto';
import { IsInt } from 'class-validator';

export class UpdateFinalGeneratedClassScheduleDto extends PartialType(
  CreateFinalGeneratedClassScheduleDto,
) {}
