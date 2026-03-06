import {
  IsInt,
  IsString,
  IsOptional,
  IsNumber,
  IsBoolean,
  IsArray,
  ArrayNotEmpty,
  ArrayUnique,
} from 'class-validator';

export class CreateFinalGeneratedClassScheduleDto {
  @IsOptional()
  @IsInt()
  class_id?: number;

  @IsOptional()
  @IsInt()
  course_id?: number;

  @IsOptional()
  @IsString()
  course_code?: string;

  @IsOptional()
  @IsInt()
  program_id?: number;

  @IsOptional()
  @IsString()
  program_code?: string;

  @IsOptional()
  @IsInt()
  institute_id?: number;

  @IsOptional()
  @IsString()
  type?: string; // Lecture, Laboratory, etc.

  @IsOptional()
  @IsString()
  day?: string; // Monday, Tuesday, etc.

  @IsOptional()
  @IsNumber({ maxDecimalPlaces: 2 })
  start_hour?: number;

  @IsOptional()
  @IsNumber()
  duration?: number;

  @IsOptional()
  @IsInt()
  room_id?: number;

  @IsOptional()
  @IsString()
  room_name?: string;

  @IsOptional()
  @IsString()
  set_name?: string;

  @IsOptional()
  @IsString()
  time_slot?: string;

  @IsOptional()
  @IsString()
  room_type?: string;

  @IsOptional()
  @IsInt()
  room_capacity?: number;

  @IsOptional()
  @IsInt()
  class_size?: number;

  @IsOptional()
  @IsInt()
  faculty_id?: number;

  @IsOptional()
  @IsString()
  faculty_name?: string;

  @IsOptional()
  @IsString()
  school_year?: string; // e.g., "2025 - 2026"

  @IsOptional()
  @IsString()
  semester?: string; // e.g., "1st"

  @IsOptional()
  @IsString()
  mode?: string;

  // -------------------------
  // Join tracking fields
  // -------------------------
  @IsOptional()
  @IsInt()
  join_group_id?: number;

  @IsOptional()
  @IsBoolean()
  is_joined?: boolean;

  @IsOptional()
  @IsArray()
  @ArrayNotEmpty()
  @ArrayUnique()
  @IsInt({ each: true })
  joined_with?: number[];
}
