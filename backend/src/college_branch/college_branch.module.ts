import { Module } from '@nestjs/common';
import { CollegeBranchService } from './college_branch.service';
import { CollegeBranchController } from './college_branch.controller';
import { TypeOrmModule } from '@nestjs/typeorm';
import { CollegeBranch } from './entities/college_branch.entity';
@Module({
  imports: [TypeOrmModule.forFeature([CollegeBranch])],
  controllers: [CollegeBranchController],
  providers: [CollegeBranchService],
})
export class CollegeBranchModule {}
