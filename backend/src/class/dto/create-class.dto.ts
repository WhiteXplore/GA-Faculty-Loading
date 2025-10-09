import { IsInt, IsString, IsNotEmpty } from 'class-validator';

export class CreateClassDto {
  @IsInt()
  @IsNotEmpty()
  school_year_id: number;

  @IsInt()
  @IsNotEmpty()
  program_id: number;

  @IsString()
  @IsNotEmpty()
  set_name: string;

  @IsInt()
  @IsNotEmpty()
  class_size: number;
}

