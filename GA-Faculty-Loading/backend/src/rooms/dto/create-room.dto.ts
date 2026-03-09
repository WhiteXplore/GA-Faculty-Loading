import { IsNumber, IsOptional, IsString } from 'class-validator';

export class CreateRoomDto {
  @IsString()
  room_name: string;

  @IsNumber()
  room_capacity: number;

  @IsString()
  room_type: string;

  @IsOptional()
  @IsNumber()
  institute_id?: number;

  @IsOptional()
  @IsNumber()
  building_id?: number;
}
