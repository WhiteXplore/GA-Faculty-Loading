import { IsString, IsInt, IsOptional, Min } from 'class-validator';

export class CreateRoomDto {
  @IsString()
  room_name: string;

  @IsInt()
  @Min(1)
  room_capacity: number;

  @IsString()
  room_type: string;

  @IsInt()
  @IsOptional()
  institute_id?: number;
}
