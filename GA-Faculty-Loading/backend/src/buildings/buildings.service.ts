import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';

import { Building } from './entities/building.entity';
import { CreateBuildingDto } from './dto/create-building.dto';
import { UpdateBuildingDto } from './dto/update-building.dto';

import { BuildingArea } from 'src/building_areas/entities/building_area.entity';

@Injectable()
export class BuildingsService {
  constructor(
    @InjectRepository(Building)
    private buildingRepository: Repository<Building>,

    @InjectRepository(BuildingArea)
    private areaRepository: Repository<BuildingArea>,
  ) {}

  async create(createBuildingDto: CreateBuildingDto) {
    const building = new Building();

    building.building_name = createBuildingDto.building_name;

    if (createBuildingDto.building_area_id) {
      const area = await this.areaRepository.findOne({
        where: { building_area_id: createBuildingDto.building_area_id },
      });

      if (area) {
        building.buildingArea = area;
      }
    }

    return await this.buildingRepository.save(building);
  }

  async findAll() {
    return await this.buildingRepository.find({
      relations: ['buildingArea', 'buildingArea.collegeBranch'],
      order: {
        building_id: 'DESC',
      },
    });
  }

  async findOne(id: number) {
    const building = await this.buildingRepository.findOne({
      where: { building_id: id },
      relations: ['buildingArea'],
    });

    if (!building) {
      throw new NotFoundException('Building not found');
    }

    return building;
  }

  async update(id: number, updateBuildingDto: UpdateBuildingDto) {
    const building = await this.buildingRepository.findOne({
      where: { building_id: id },
    });

    if (!building) {
      throw new NotFoundException('Building not found');
    }

    if (updateBuildingDto.building_name) {
      building.building_name = updateBuildingDto.building_name;
    }

    if (updateBuildingDto.building_area_id) {
      const area = await this.areaRepository.findOne({
        where: { building_area_id: updateBuildingDto.building_area_id },
      });

      if (area) {
        building.buildingArea = area;
      }
    }

    return await this.buildingRepository.save(building);
  }

  async remove(id: number) {
    return await this.buildingRepository.delete(id);
  }
}
