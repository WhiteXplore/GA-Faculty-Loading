// create-calendar.dto.ts
import { IsString, IsDateString, IsBoolean, IsOptional } from 'class-validator';

export class CreateCalendarDto {
  @IsString()
  title: string;

  @IsDateString()
  startDate: string;

  @IsDateString()
  endDate: string;

  @IsOptional()
  @IsString()
  timeStart?: string;

  @IsOptional()
  @IsString()
  timeEnd?: string;

  @IsBoolean()
  isAllDay: boolean;
}
