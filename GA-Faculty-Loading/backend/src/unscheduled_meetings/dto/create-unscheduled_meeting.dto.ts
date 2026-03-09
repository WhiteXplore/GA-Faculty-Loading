import { IsString, IsNumber } from 'class-validator';

export class CreateUnscheduledMeetingDto {
  @IsNumber()
  class_id: number;

  @IsString()
  course_code: string;

  @IsNumber()
  program_id: number;

  @IsString()
  program_code: string;

  @IsString()
  type: string;

  @IsString()
  hours: string;

  @IsString()
  reason: string;

  // ✅ ADD THESE
  @IsString()
  school_year: string;

  @IsString()
  semester: string;
}
