import { IsString, IsInt, IsOptional, Min } from 'class-validator';

export class CreateRoomDto {
  @IsOptional()
  @IsString()
  building_name: string;

  @IsOptional()
  @IsString()
  room_name: string;

  @IsOptional()
  @IsInt()
  @Min(1)
  room_capacity: number;

  @IsOptional()
  @IsString()
  room_type: string;

  @IsInt()
  @IsOptional()
  institute_id?: number;
}
