import { Injectable } from '@nestjs/common';
import { CreateBuildingAreaDto } from './dto/create-building_area.dto';
import { UpdateBuildingAreaDto } from './dto/update-building_area.dto';

@Injectable()
export class BuildingAreasService {
  create(createBuildingAreaDto: CreateBuildingAreaDto) {
    return 'This action adds a new buildingArea';
  }

  findAll() {
    return `This action returns all buildingAreas`;
  }

  findOne(id: number) {
    return `This action returns a #${id} buildingArea`;
  }

  update(id: number, updateBuildingAreaDto: UpdateBuildingAreaDto) {
    return `This action updates a #${id} buildingArea`;
  }

  remove(id: number) {
    return `This action removes a #${id} buildingArea`;
  }
}
