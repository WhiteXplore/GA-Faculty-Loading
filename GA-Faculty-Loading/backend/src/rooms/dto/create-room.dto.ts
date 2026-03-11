import { IsNumber, IsOptional, IsString } from 'class-validator';
import { Type } from 'class-transformer';

export class CreateRoomDto {
  @IsString()
  room_name: string;

  @Type(() => Number)
  @IsNumber()
  room_capacity: number;

  @IsString()
  room_type: string;

  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  institute_id?: number | null;

  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  building_id?: number | null;
}
