import { Module } from '@nestjs/common';
import { BuildingsService } from './buildings.service';
import { BuildingsController } from './buildings.controller';
import { Building } from './entities/building.entity';
import { TypeOrmModule } from '@nestjs/typeorm';
import { CollegeBranch } from 'src/college_branch/entities/college_branch.entity';
@Module({
  imports: [TypeOrmModule.forFeature([Building, CollegeBranch])],
  controllers: [BuildingsController],
  providers: [BuildingsService],
})
export class BuildingsModule {}
