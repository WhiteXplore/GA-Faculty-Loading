import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { ActiveSem } from './entities/active_sem.entity';
import { CreateActiveSemDto } from './dto/create-active_sem.dto';

@Injectable()
export class ActiveSemService {
  constructor(
    @InjectRepository(ActiveSem)
    private readonly activeSemRepo: Repository<ActiveSem>,
  ) {}

  async create(createActiveSemDto: CreateActiveSemDto) {
    // Deactivate all previous semesters
    await this.activeSemRepo.update({}, { is_active: false });

    // Create new active semester
    const newActiveSem = this.activeSemRepo.create({
      semester: createActiveSemDto.semester,
      is_active: true,
    });
    return await this.activeSemRepo.save(newActiveSem);
  }

  async findActive() {
    const active = await this.activeSemRepo.findOne({
      where: { is_active: true },
    });
    return active || { semester: 1 }; // default to 1st Semester if none
  }

  async findAll() {
    return await this.activeSemRepo.find();
  }

  async findOne(id: number) {
    return await this.activeSemRepo.findOneBy({ id });
  }

  async remove(id: number) {
    await this.activeSemRepo.delete(id);
    return { message: `Active semester ${id} removed.` };
  }
}
