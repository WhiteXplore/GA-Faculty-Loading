import { PartialType } from '@nestjs/swagger';
import { CreateFinalGeneratedClassScheduleDto } from './create-final_generated_class_schedule.dto';

export class UpdateFinalGeneratedClassScheduleDto extends PartialType(
  CreateFinalGeneratedClassScheduleDto,
) {}
