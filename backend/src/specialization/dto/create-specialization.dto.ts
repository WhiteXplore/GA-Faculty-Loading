import { IsInt, IsString, IsNotEmpty, IsOptional } from 'class-validator';

export class CreateSpecializationDto {
  @IsInt()
  @IsNotEmpty()
  program_id: number;

  @IsString()
  @IsNotEmpty()
  specialization_name: string;
}

