import {
  IsNotEmpty,
  IsString,
  MaxLength,
  IsNumber,
  IsOptional,
} from 'class-validator';

export class CreateBuildingAreaDto {
  @IsString()
  @IsNotEmpty()
  @MaxLength(150)
  area_name: string;

  @IsNumber()
  @IsOptional()
  time_travel: number;

  @IsNumber()
  @IsNotEmpty()
  college_branch_id: number;
}
