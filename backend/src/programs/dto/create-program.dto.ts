// src/programs/dto/create-program.dto.ts
import { IsInt, IsNotEmpty, IsOptional, IsString } from 'class-validator';

export class CreateProgramDto {
  @IsString()
  @IsNotEmpty()
  program_name: string;

  @IsString()
  @IsNotEmpty()
  program_code: string;

  @IsInt()
  @IsOptional()
  institute_id?: number; // allow linking program to institute
}
