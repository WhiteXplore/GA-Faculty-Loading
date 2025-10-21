import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { ProgramYearCourse } from './entities/program_year_course.entity';
import { CreateProgramYearCourseDto } from './dto/create-program_year_course.dto';
import { UpdateProgramYearCourseDto } from './dto/update-program_year_course.dto';

@Injectable()
export class ProgramYearCoursesService {
  constructor(
    @InjectRepository(ProgramYearCourse)
    private programYearCourseRepository: Repository<ProgramYearCourse>,
  ) {}

  async create(
    createDto: CreateProgramYearCourseDto,
  ): Promise<ProgramYearCourse> {
    const programYearCourse =
      this.programYearCourseRepository.create(createDto);
    return await this.programYearCourseRepository.save(programYearCourse);
  }

  async createBulk(
    createDtos: CreateProgramYearCourseDto[],
  ): Promise<ProgramYearCourse[]> {
    const programYearCourses = createDtos.map((dto) =>
      this.programYearCourseRepository.create(dto),
    );
    return await this.programYearCourseRepository.save(programYearCourses);
  }

  async findAll(): Promise<ProgramYearCourse[]> {
    return await this.programYearCourseRepository.find({
      relations: [
        'program',
        'program.institute',
        'course',
        'schoolYear',
        'course.curriculum',
      ],
    });
  }

  async findByProgramAndSchoolYear(
    programId: number,
    schoolYearId: number,
  ): Promise<ProgramYearCourse[]> {
    return await this.programYearCourseRepository.find({
      where: {
        program_id: programId,
        school_year_id: schoolYearId,
      },
      relations: [
        'program',
        'program.institute',
        'course',
        'schoolYear',
        'course.curriculum',
      ],
      order: {
        year_level: 'ASC',
        course: {
          course_code: 'ASC',
        },
      },
    });
  }

  async findByProgramYearLevelAndSchoolYear(
    programId: number,
    yearLevel: number,
    schoolYearId: number,
  ): Promise<ProgramYearCourse[]> {
    return await this.programYearCourseRepository.find({
      where: {
        program_id: programId,
        year_level: yearLevel,
        school_year_id: schoolYearId,
      },
      relations: [
        'program',
        'program.institute',
        'course',
        'schoolYear',
        'course.curriculum',
      ],
    });
  }

  async findOne(id: number): Promise<ProgramYearCourse | null> {
    return await this.programYearCourseRepository.findOne({
      where: { id },
      relations: ['program', 'program.institute', 'course', 'schoolYear'],
    });
  }

  async update(
    id: number,
    updateDto: UpdateProgramYearCourseDto,
  ): Promise<ProgramYearCourse | null> {
    await this.programYearCourseRepository.update(id, updateDto);
    return this.findOne(id);
  }

  async remove(id: number): Promise<void> {
    await this.programYearCourseRepository.delete(id);
  }

  async removeByProgramYearLevelAndSchoolYear(
    programId: number,
    yearLevel: number,
    schoolYearId: number,
  ): Promise<void> {
    await this.programYearCourseRepository.delete({
      program_id: programId,
      year_level: yearLevel,
      school_year_id: schoolYearId,
    });
  }
}
