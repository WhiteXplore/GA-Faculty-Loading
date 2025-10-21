import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { SelectedYearSem } from './entities/selected-year-sem.entity';
import { CreateSelectedYearSemDto } from './dto/create-selected-year-sem.dto';
import { UpdateSelectedYearSemDto } from './dto/update-selected-year-sem.dto';

@Injectable()
export class SelectedYearSemService {
  constructor(
    @InjectRepository(SelectedYearSem)
    private readonly selectedYearSemRepo: Repository<SelectedYearSem>,
  ) {}

  async create(createSelectedYearSemDto: CreateSelectedYearSemDto) {
    // Optional: Replace old record so only one is saved
    await this.selectedYearSemRepo.clear();
    const record = this.selectedYearSemRepo.create(createSelectedYearSemDto);
    return this.selectedYearSemRepo.save(record);
  }

  findAll() {
    return this.selectedYearSemRepo.find();
  }

  findOne(id: number) {
    return this.selectedYearSemRepo.findOne({ where: { id } });
  }

  update(id: number, updateSelectedYearSemDto: UpdateSelectedYearSemDto) {
    return this.selectedYearSemRepo.update(id, updateSelectedYearSemDto);
  }

  remove(id: number) {
    return this.selectedYearSemRepo.delete(id);
  }
}
