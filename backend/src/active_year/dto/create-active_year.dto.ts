import { IsInt, IsBoolean, IsOptional } from 'class-validator';

export class CreateActiveYearDto {
  @IsInt()
  year: number;

  @IsBoolean()
  @IsOptional()
  isActive?: boolean = true;
}
