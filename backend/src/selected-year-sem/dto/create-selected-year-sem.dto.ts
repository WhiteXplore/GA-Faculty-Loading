import { IsInt, IsString, IsNotEmpty } from 'class-validator';

export class CreateSelectedYearSemDto {
  @IsString()
  @IsNotEmpty()
  year: string;

  @IsInt()
  @IsNotEmpty()
  semester: number;
}
