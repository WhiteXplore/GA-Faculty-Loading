import { PartialType } from '@nestjs/swagger';
import { CreateGeneratedScheduledDto } from './create-generated_scheduled.dto';

export class UpdateGeneratedScheduledDto extends PartialType(CreateGeneratedScheduledDto) {}
