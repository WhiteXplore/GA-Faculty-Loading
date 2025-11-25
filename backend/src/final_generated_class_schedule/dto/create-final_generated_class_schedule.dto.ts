import { IsInt, IsString, IsOptional } from 'class-validator';

export class CreateFinalGeneratedClassScheduleDto {
  @IsInt()
  @IsOptional()
  class_id?: number;

  @IsString()
  @IsOptional()
  course_code?: string;

  @IsInt()
  @IsOptional()
  program_id?: number;

  @IsInt()
  @IsOptional()
  institute_id?: number;

  @IsString()
  @IsOptional()
  type?: string; // Lecture, Lab, etc.

  @IsString()
  @IsOptional()
  day?: string; // e.g., Monday

  @IsInt()
  @IsOptional()
  start_hour?: number;

  @IsInt()
  @IsOptional()
  duration?: number;

  @IsString()
  @IsOptional()
  time_slot?: string; // e.g., "8:00 AM - 11:00 AM"

  @IsInt()
  @IsOptional()
  room_id?: number;

  @IsString()
  @IsOptional()
  room_name?: string;

  @IsString()
  @IsOptional()
  room_type?: string;

  @IsInt()
  @IsOptional()
  room_capacity?: number;

  @IsInt()
  @IsOptional()
  class_size?: number;

  @IsInt()
  @IsOptional()
  faculty_id?: number;

  @IsString()
  @IsOptional()
  faculty_name?: string;

  @IsString()
  @IsOptional()
  school_year?: string;
}
