import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { AssignClass } from './entities/assign_class.entity';
import { CreateAssignClassDto } from './dto/create-assign_class.dto';
import { UpdateAssignClassDto } from './dto/update-assign_class.dto';

@Injectable()
export class AssignClassService {
  constructor(
    @InjectRepository(AssignClass)
    private assignClassRepo: Repository<AssignClass>,
  ) {}

  create(createAssignClassDto: CreateAssignClassDto) {
    const newAssignClass = this.assignClassRepo.create(createAssignClassDto);
    return this.assignClassRepo.save(newAssignClass);
  }

  findAll() {
    return this.assignClassRepo.find({
      relations: {
        program: {
          institute: true, // <-- nested relation
        },
        course: {
          curriculum: true,
        },
      },
    });
  }

  findOne(id: number) {
    return this.assignClassRepo.findOne({
      where: { assign_class_id: id },
      relations: {
        program: {
          institute: true,
        },
        course: true,
      },
    });
  }

  update(id: number, updateAssignClassDto: UpdateAssignClassDto) {
    return this.assignClassRepo.update(id, updateAssignClassDto);
  }

  remove(id: number) {
    return this.assignClassRepo.delete(id);
  }
}
