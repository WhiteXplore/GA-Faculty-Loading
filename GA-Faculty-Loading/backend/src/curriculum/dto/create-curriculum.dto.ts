import { IsInt } from 'class-validator';
import { Type } from 'class-transformer';

export class CreateCurriculumDto {
  @Type(() => Number)
  @IsInt()
  curriculum_start_year: number;

  @Type(() => Number)
  @IsInt()
  curriculum_end_year: number;

  @Type(() => Number)
  @IsInt()
  institute_id: number;

  @Type(() => Number)
  @IsInt()
  program_id: number;
}
