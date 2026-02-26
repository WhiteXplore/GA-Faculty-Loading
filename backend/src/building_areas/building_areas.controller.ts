import { Controller, Get, Post, Body, Patch, Param, Delete } from '@nestjs/common';
import { BuildingAreasService } from './building_areas.service';
import { CreateBuildingAreaDto } from './dto/create-building_area.dto';
import { UpdateBuildingAreaDto } from './dto/update-building_area.dto';

@Controller('building-areas')
export class BuildingAreasController {
  constructor(private readonly buildingAreasService: BuildingAreasService) {}

  @Post()
  create(@Body() createBuildingAreaDto: CreateBuildingAreaDto) {
    return this.buildingAreasService.create(createBuildingAreaDto);
  }

  @Get()
  findAll() {
    return this.buildingAreasService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.buildingAreasService.findOne(+id);
  }

  @Patch(':id')
  update(@Param('id') id: string, @Body() updateBuildingAreaDto: UpdateBuildingAreaDto) {
    return this.buildingAreasService.update(+id, updateBuildingAreaDto);
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.buildingAreasService.remove(+id);
  }
}
