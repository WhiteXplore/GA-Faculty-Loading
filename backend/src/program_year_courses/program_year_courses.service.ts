import { Injectable } from '@nestjs/common';
import { InjectRepository, InjectDataSource } from '@nestjs/typeorm';
import { Repository, DataSource } from 'typeorm';
import { ProgramYearCourse } from './entities/program_year_course.entity';
import { CreateProgramYearCourseDto } from './dto/create-program_year_course.dto';
import { UpdateProgramYearCourseDto } from './dto/update-program_year_course.dto';

@Injectable()
export class ProgramYearCoursesService {
  constructor(
    @InjectRepository(ProgramYearCourse)
    private programYearCourseRepository: Repository<ProgramYearCourse>,
    @InjectDataSource() private dataSource: DataSource,
  ) {}

  async create(
    createDto: CreateProgramYearCourseDto,
  ): Promise<ProgramYearCourse> {
    const programYearCourse =
      this.programYearCourseRepository.create(createDto);
    return await this.programYearCourseRepository.save(programYearCourse);
  }

  async syncProgramYearCoursesFromClasses(): Promise<void> {
    const sql = `
 INSERT INTO dnsc_class_scheduler.program_year_courses
    (program_id, course_id, year_level, school_year_id, created_at, updated_at)
SELECT
    cl.program_id,
    cr.course_id,
    CASE
        WHEN cl.set_name LIKE '1st Year%' THEN 1
        WHEN cl.set_name LIKE '2nd Year%' THEN 2
        WHEN cl.set_name LIKE '3rd Year%' THEN 3
        WHEN cl.set_name LIKE '4th Year%' THEN 4
    END AS year_level,
    cl.school_year_id,
    NOW() AS created_at,
    NOW() AS updated_at
FROM dnsc_class_scheduler.classes cl
JOIN dnsc_class_scheduler.courses cr
    ON cr.program_id = cl.program_id
    AND cr.course_level = CASE
        WHEN cl.set_name LIKE '1st Year%' THEN 1
        WHEN cl.set_name LIKE '2nd Year%' THEN 2
        WHEN cl.set_name LIKE '3rd Year%' THEN 3
        WHEN cl.set_name LIKE '4th Year%' THEN 4
    END
WHERE NOT EXISTS (
    SELECT 1
    FROM dnsc_class_scheduler.program_year_courses pyc
    WHERE pyc.program_id = cl.program_id
      AND pyc.course_id = cr.course_id
      AND pyc.year_level = CASE
        WHEN cl.set_name LIKE '1st Year%' THEN 1
        WHEN cl.set_name LIKE '2nd Year%' THEN 2
        WHEN cl.set_name LIKE '3rd Year%' THEN 3
        WHEN cl.set_name LIKE '4th Year%' THEN 4
      END
      AND pyc.school_year_id = cl.school_year_id
);


    `;

    await this.dataSource.query(sql);
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

  async findFromView(): Promise<any[]> {
    const sql = 'SELECT * FROM dnsc_class_scheduler.vw_program_year_courses';
    return await this.dataSource.query(sql);
  }

  async findByProgramAndSchoolYear(
    programId: number,
    schoolYearId: number,
  ): Promise<ProgramYearCourse[]> {
    return await this.programYearCourseRepository.find({
      where: { program_id: programId, school_year_id: schoolYearId },
      relations: [
        'program',
        'program.institute',
        'course',
        'schoolYear',
        'course.curriculum',
      ],
      order: {
        year_level: 'ASC',
        course: { course_code: 'ASC' },
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

  // 🔹 AUTOMATIC SYNC METHOD
  async syncFromCourses(): Promise<ProgramYearCourse[]> {
    const courses: any[] = await this.dataSource.query(`
      SELECT 
        c.course_id,
        c.program_id
      FROM courses c
      WHERE c.program_id IS NOT NULL
    `);

    if (!courses.length) return [];

    const programYearCourses = courses.map((c) => ({
      program_id: c.program_id,
      course_id: c.course_id,
      year_level: 1, // You can adjust logic based on course or curriculum
      school_year_id: 1, // Replace with current school year ID dynamically if needed
    }));

    const created = this.programYearCourseRepository.create(programYearCourses);
    return await this.programYearCourseRepository.save(created);
  }
}
