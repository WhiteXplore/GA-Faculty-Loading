import { IsInt, IsNotEmpty, Min, Max } from 'class-validator';

export class CreateProgramYearCourseDto {
  @IsInt()
  @IsNotEmpty()
  program_id: number;

  @IsInt()
  @IsNotEmpty()
  course_id: number;

  @IsInt()
  @IsNotEmpty()
  @Min(1)
  @Max(4)
  year_level: number;

  @IsInt()
  @IsNotEmpty()
  school_year_id: number;
}
