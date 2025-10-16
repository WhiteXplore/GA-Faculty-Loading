import { IsString, IsInt, IsBoolean, IsOptional } from 'class-validator';

export class CreateSchoolYearDto {
  @IsString()
  school_year_name: string;

  @IsInt()
  start_year: number;

  @IsInt()
  end_year: number;

  @IsInt()
  semester: number;

  @IsBoolean()
  @IsOptional()
  is_active?: boolean;
}

