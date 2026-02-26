import { Module } from '@nestjs/common';
import { BuildingAreasService } from './building_areas.service';
import { BuildingAreasController } from './building_areas.controller';
import { BuildingArea } from './entities/building_area.entity';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Building } from 'src/buildings/entities/building.entity';
@Module({
  imports: [TypeOrmModule.forFeature([BuildingArea, Building])],
  controllers: [BuildingAreasController],
  providers: [BuildingAreasService],
})
export class BuildingAreasModule {}
