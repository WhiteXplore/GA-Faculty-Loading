import {
  IsString,
  IsInt,
  IsBoolean,
  IsOptional,
  Min,
  Max,
} from 'class-validator';

export class CreateSchoolYearDto {
  @IsString()
  school_year_name: string; // e.g., "2024-2025"

  @IsInt()
  @Min(2000)
  @Max(2100)
  start_year: number; // e.g., 2024

  @IsInt()
  @Min(2000)
  @Max(2100)
  end_year: number; // e.g., 2025

  @IsInt()
  @Min(1)
  @Max(2)
  semester: number; // 1 or 2

  @IsBoolean()
  @IsOptional()
  is_active?: boolean; // optional, default false
}
