import { IsNumber, IsOptional } from 'class-validator';

export class CreateFacultyBranchDto {
  @IsOptional()
  @IsNumber()
  user_id: number;
  @IsOptional()
  @IsNumber()
  college_branch_id: number;
}
