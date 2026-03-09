import { IsNotEmpty, IsString, MaxLength } from 'class-validator';

export class CreateCollegeBranchDto {
  @IsNotEmpty()
  @IsString()
  @MaxLength(100)
  college_branch_name: string;
}
