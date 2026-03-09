import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository, DataSource } from 'typeorm';
import { Instructor } from './entities/instructor.entity';
import { InstructorExpertise } from './entities/instructor_expertise.entity';
import { CreateInstructorDto } from './dto/create-instructor.dto';
import { UpdateInstructorDto } from './dto/update-instructor.dto';
import { classToPlain } from 'class-transformer';

@Injectable()
export class InstructorsService {
  constructor(
    @InjectRepository(Instructor)
    private readonly instructorRepository: Repository<Instructor>,
    @InjectRepository(InstructorExpertise)
    private readonly expertiseRepository: Repository<InstructorExpertise>,
    private readonly dataSource: DataSource,
  ) {}

  async create(createInstructorDto: CreateInstructorDto): Promise<any> {
    const { instructor_expertise, ...instructorData } = createInstructorDto;

    const instructor = this.instructorRepository.create(instructorData);
    await this.instructorRepository.save(instructor);

    if (instructor_expertise?.length) {
      const expertiseEntities = instructor_expertise.map((exp) => {
        const expertise = this.expertiseRepository.create({
          expertise: exp,
          instructor: instructor,
        });
        return expertise;
      });
      await this.expertiseRepository.save(expertiseEntities);
    }

    const savedInstructor = await this.findOne(instructor.instructor_id);
    return classToPlain(savedInstructor); // safe JSON
  }

  async findAll(): Promise<any> {
    const instructors = await this.instructorRepository.find({
      relations: ['institute', 'program', 'expertise'],
    });
    return classToPlain(instructors); // prevents circular JSON
  }

  async findOne(id: number): Promise<any> {
    const instructor = await this.instructorRepository.findOne({
      where: { instructor_id: id },
      relations: ['institute', 'program', 'expertise'],
    });
    if (!instructor) {
      throw new NotFoundException(`Instructor with ID ${id} not found`);
    }
    return classToPlain(instructor);
  }

  async findAllFaculty(): Promise<any> {
    const instructors = await this.dataSource.query(
      `SELECT * FROM dnsc_class_scheduler.faculty;`,
    );
    return instructors;
  }

  async update(
    id: number,
    updateInstructorDto: UpdateInstructorDto,
  ): Promise<any> {
    const { instructor_expertise, ...instructorData } = updateInstructorDto;

    const instructor = await this.instructorRepository.preload({
      instructor_id: id,
      ...instructorData,
    });

    if (!instructor) {
      throw new NotFoundException(`Instructor with ID ${id} not found`);
    }

    if (instructor_expertise) {
      // Remove old expertise
      await this.expertiseRepository.delete({ instructor_id: id });

      const expertiseEntities = instructor_expertise.map((exp) =>
        this.expertiseRepository.create({ expertise: exp, instructor }),
      );
      await this.expertiseRepository.save(expertiseEntities);
    }

    const updatedInstructor = await this.instructorRepository.save(instructor);
    return classToPlain(updatedInstructor);
  }

  async remove(id: number): Promise<void> {
    const result = await this.instructorRepository.delete(id);
    if (result.affected === 0) {
      throw new NotFoundException(`Instructor with ID ${id} not found`);
    }
  }
}
