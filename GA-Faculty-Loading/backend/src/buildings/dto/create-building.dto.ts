import { IsOptional, IsString, IsInt } from 'class-validator';

export class CreateBuildingDto {
  @IsString()
  building_name: string;

  @IsOptional()
  @IsInt()
  building_area_id?: number;
}
