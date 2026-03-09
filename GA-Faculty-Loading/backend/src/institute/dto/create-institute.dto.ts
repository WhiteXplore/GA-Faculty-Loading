import { IsString } from 'class-validator';

export class CreateInstituteDto {
  @IsString()
  institute_name: string;

  @IsString()
  institute_code: string;
}
