import { PartialType } from '@nestjs/mapped-types';
import { CreateProgramYearCourseDto } from './create-program_year_course.dto';

export class UpdateProgramYearCourseDto extends PartialType(
  CreateProgramYearCourseDto,
) {}








