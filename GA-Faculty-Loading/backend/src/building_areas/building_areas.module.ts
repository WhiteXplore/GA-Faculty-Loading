import { Module } from '@nestjs/common';
import { BuildingAreasService } from './building_areas.service';
import { BuildingAreasController } from './building_areas.controller';
import { TypeOrmModule } from '@nestjs/typeorm';
import { BuildingArea } from './entities/building_area.entity';
import { CollegeBranch } from 'src/college_branch/entities/college_branch.entity';

@Module({
  imports: [TypeOrmModule.forFeature([BuildingArea, CollegeBranch])],
  controllers: [BuildingAreasController],
  providers: [BuildingAreasService],
})
export class BuildingAreasModule {}
