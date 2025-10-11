import { IsInt, IsOptional, Min, Max } from 'class-validator';

export class CreateActiveSemDto {
  @IsInt()
  @Min(1)
  @Max(3)
  semester: number;

  @IsOptional()
  is_active?: boolean;
}
