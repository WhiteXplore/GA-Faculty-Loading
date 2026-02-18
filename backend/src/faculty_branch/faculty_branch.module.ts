import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';

import { FacultyBranch } from './entities/faculty_branch.entity';
import { FacultyBranchService } from './faculty_branch.service';
import { FacultyBranchController } from './faculty_branch.controller';
import { User_Accounts } from 'src/user/entities/user.entity';
import { CollegeBranch } from 'src/college_branch/entities/college_branch.entity';

@Module({
  imports: [
    TypeOrmModule.forFeature([FacultyBranch, User_Accounts, CollegeBranch]),
  ],
  controllers: [FacultyBranchController],
  providers: [FacultyBranchService],
  exports: [FacultyBranchService],
})
export class FacultyBranchModule {}
