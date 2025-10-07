import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { ActiveYear } from './entities/active_year.entity';
import { CreateActiveYearDto } from './dto/create-active_year.dto';
import { UpdateActiveYearDto } from './dto/update-active_year.dto';

@Injectable()
export class ActiveYearService {
  constructor(
    @InjectRepository(ActiveYear)
    private readonly activeYearRepository: Repository<ActiveYear>,
  ) {}

  async setActiveYear(
    createActiveYearDto: CreateActiveYearDto,
  ): Promise<ActiveYear> {
    const { year } = createActiveYearDto;

    // deactivate all years
    await this.activeYearRepository.update({}, { isActive: false });

    // check if year exists
    let existingYear = await this.activeYearRepository.findOne({
      where: { year },
    });

    if (existingYear) {
      // just activate it
      existingYear.isActive = true;
      return this.activeYearRepository.save(existingYear);
    }

    // if not exists, create it as active
    const activeYear = this.activeYearRepository.create({
      year,
      isActive: true,
    });
    return this.activeYearRepository.save(activeYear);
  }

  async findAll(): Promise<ActiveYear[]> {
    return this.activeYearRepository.find();
  }

  async findOne(id: number): Promise<ActiveYear> {
    const year = await this.activeYearRepository.findOneBy({ id });
    if (!year) {
      throw new NotFoundException(`ActiveYear with id ${id} not found`);
    }
    return year;
  }

  async update(
    id: number,
    updateActiveYearDto: UpdateActiveYearDto,
  ): Promise<ActiveYear> {
    await this.activeYearRepository.update(id, updateActiveYearDto);
    return this.findOne(id);
  }

  async remove(id: number): Promise<void> {
    await this.activeYearRepository.delete(id);
  }

  // ✅ helper to get current active year
  async getActiveYear(): Promise<ActiveYear | null> {
    return this.activeYearRepository.findOne({ where: { isActive: true } });
  }
}
