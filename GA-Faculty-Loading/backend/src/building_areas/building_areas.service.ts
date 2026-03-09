import { Injectable, NotFoundException } from '@nestjs/common';
import { CreateBuildingAreaDto } from './dto/create-building_area.dto';
import { UpdateBuildingAreaDto } from './dto/update-building_area.dto';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';

import { BuildingArea } from './entities/building_area.entity';
import { CollegeBranch } from 'src/college_branch/entities/college_branch.entity';

@Injectable()
export class BuildingAreasService {
  constructor(
    @InjectRepository(BuildingArea)
    private readonly buildingAreaRepository: Repository<BuildingArea>,

    @InjectRepository(CollegeBranch)
    private readonly branchRepository: Repository<CollegeBranch>,
  ) {}

  async create(createBuildingAreaDto: CreateBuildingAreaDto) {
    const branch = await this.branchRepository.findOne({
      where: { college_branch_id: createBuildingAreaDto.college_branch_id },
    });

    if (!branch) {
      throw new NotFoundException('College branch not found');
    }

    const area = this.buildingAreaRepository.create({
      area_name: createBuildingAreaDto.area_name,
      time_travel: createBuildingAreaDto.time_travel,
      collegeBranch: branch,
    });

    return await this.buildingAreaRepository.save(area);
  }

  async findAll() {
    return await this.buildingAreaRepository.find({
      relations: ['collegeBranch'],
      order: {
        area_name: 'ASC',
      },
    });
  }

  async findOne(id: number) {
    const area = await this.buildingAreaRepository.findOne({
      where: { building_area_id: id },
      relations: ['collegeBranch'],
    });

    if (!area) {
      throw new NotFoundException('Building area not found');
    }

    return area;
  }

  async update(id: number, updateDto: UpdateBuildingAreaDto) {
    const area = await this.findOne(id);

    if (updateDto.college_branch_id) {
      const branch = await this.branchRepository.findOne({
        where: { college_branch_id: updateDto.college_branch_id },
      });

      if (!branch) {
        throw new NotFoundException('College branch not found');
      }

      area.collegeBranch = branch;
    }

    area.area_name = updateDto.area_name ?? area.area_name;
    area.time_travel = updateDto.time_travel ?? area.time_travel;

    return await this.buildingAreaRepository.save(area);
  }

  async remove(id: number) {
    const area = await this.findOne(id);

    await this.buildingAreaRepository.remove(area);

    return {
      message: 'Building area deleted successfully',
    };
  }
}
