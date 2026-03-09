import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
  ParseIntPipe,
} from '@nestjs/common';

import { BuildingAreasService } from './building_areas.service';
import { CreateBuildingAreaDto } from './dto/create-building_area.dto';
import { UpdateBuildingAreaDto } from './dto/update-building_area.dto';

@Controller('building-areas')
export class BuildingAreasController {
  constructor(private readonly buildingAreasService: BuildingAreasService) {}

  // CREATE
  @Post('add-building-areas')
  create(@Body() createBuildingAreaDto: CreateBuildingAreaDto) {
    return this.buildingAreasService.create(createBuildingAreaDto);
  }

  // GET ALL
  @Get('get-all-building-areas')
  findAll() {
    return this.buildingAreasService.findAll();
  }

  // GET ONE
  @Get(':id')
  findOne(@Param('id', ParseIntPipe) id: number) {
    return this.buildingAreasService.findOne(id);
  }

  // UPDATE
  @Patch(':id')
  update(
    @Param('id', ParseIntPipe) id: number,
    @Body() updateBuildingAreaDto: UpdateBuildingAreaDto,
  ) {
    return this.buildingAreasService.update(id, updateBuildingAreaDto);
  }

  // DELETE
  @Delete(':id')
  remove(@Param('id', ParseIntPipe) id: number) {
    return this.buildingAreasService.remove(id);
  }
}
