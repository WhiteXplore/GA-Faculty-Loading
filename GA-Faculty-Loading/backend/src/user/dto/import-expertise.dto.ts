import { IsNotEmpty, IsString } from 'class-validator';

export class ImportExpertiseDto {
  @IsNotEmpty()
  @IsString()
  instructor_name: string;

  @IsNotEmpty()
  @IsString()
  course_code: string;
}


