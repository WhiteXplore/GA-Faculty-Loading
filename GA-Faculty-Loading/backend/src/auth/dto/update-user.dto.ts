import {
  IsOptional,
  IsString,
  IsEmail,
  IsNumber,
  IsArray,
} from 'class-validator';

export class UpdateUserDto {
  @IsOptional()
  @IsString()
  first_name?: string;

  @IsOptional()
  @IsString()
  last_name?: string;

  @IsOptional()
  @IsEmail()
  email?: string;

  @IsOptional()
  @IsString()
  password?: string;

  @IsOptional()
  @IsString()
  role?: string;

  @IsOptional()
  @IsNumber()
  institute_id?: number;

  @IsOptional()
  @IsNumber()
  program_id?: number;

  @IsOptional()
  @IsNumber()
  school_year_id?: number;

  // ✅ Allow array of course IDs for expertise
  @IsOptional()
  @IsArray()
  expertise?: number[];

  // ✅ Allow array of course IDs for other expertise
  @IsOptional()
  @IsArray()
  other_expertise?: number[];
}
