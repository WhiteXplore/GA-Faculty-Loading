import { PartialType } from '@nestjs/swagger';
import { CreateCollegeBranchDto } from './create-college_branch.dto';

export class UpdateCollegeBranchDto extends PartialType(CreateCollegeBranchDto) {}
