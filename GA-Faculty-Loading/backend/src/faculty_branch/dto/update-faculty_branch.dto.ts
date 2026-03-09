import { PartialType } from '@nestjs/swagger';
import { CreateFacultyBranchDto } from './create-faculty_branch.dto';

export class UpdateFacultyBranchDto extends PartialType(CreateFacultyBranchDto) {}
