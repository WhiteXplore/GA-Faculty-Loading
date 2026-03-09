import { PartialType } from '@nestjs/swagger';
import { CreateSelectedYearSemDto } from './create-selected-year-sem.dto';

export class UpdateSelectedYearSemDto extends PartialType(CreateSelectedYearSemDto) {}
