import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Curriculum } from './entities/curriculum.entity';
import { CreateCurriculumDto } from './dto/create-curriculum.dto';
import { UpdateCurriculumDto } from './dto/update-curriculum.dto';

@Injectable()
export class CurriculumService {
  constructor(
    @InjectRepository(Curriculum)
    private readonly curriculumRepository: Repository<Curriculum>,
  ) {}

  async create(createCurriculumDto: CreateCurriculumDto): Promise<Curriculum> {
    const existing = await this.curriculumRepository.findOne({
      where: {
        institute_id: createCurriculumDto.institute_id,
        program_id: createCurriculumDto.program_id,
        curriculum_start_year: createCurriculumDto.curriculum_start_year,
        curriculum_end_year: createCurriculumDto.curriculum_end_year,
      },
    });

    if (existing) {
      return existing;
    }

    const newCurriculum = this.curriculumRepository.create(createCurriculumDto);

    return await this.curriculumRepository.save(newCurriculum);
  }
  async findAll(): Promise<Curriculum[]> {
    return await this.curriculumRepository.find({
      relations: ['program', 'program.institute'],
    });
  }

  async findOne(id: number): Promise<Curriculum> {
    const curriculum = await this.curriculumRepository.findOne({
      where: { curriculum_id: id },
      relations: ['program'],
    });

    if (!curriculum) {
      throw new NotFoundException(`Curriculum with ID ${id} not found`);
    }

    return curriculum;
  }

  async update(
    id: number,
    updateCurriculumDto: UpdateCurriculumDto,
  ): Promise<Curriculum> {
    const curriculum = await this.findOne(id);
    const updated = Object.assign(curriculum, updateCurriculumDto);
    return await this.curriculumRepository.save(updated);
  }

  async remove(id: number): Promise<void> {
    const curriculum = await this.findOne(id);
    await this.curriculumRepository.remove(curriculum);
  }
}
