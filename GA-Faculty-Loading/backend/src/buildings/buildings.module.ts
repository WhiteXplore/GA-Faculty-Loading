import { Module } from '@nestjs/common';
import { BuildingsService } from './buildings.service';
import { BuildingsController } from './buildings.controller';
import { Building } from './entities/building.entity';
import { TypeOrmModule } from '@nestjs/typeorm';

import { BuildingArea } from 'src/building_areas/entities/building_area.entity';
@Module({
  imports: [TypeOrmModule.forFeature([Building, BuildingArea])],
  controllers: [BuildingsController],
  providers: [BuildingsService],
})
export class BuildingsModule {}
