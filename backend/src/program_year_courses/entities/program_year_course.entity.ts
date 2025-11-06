import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  ManyToOne,
  JoinColumn,
} from 'typeorm';
import { Program } from 'src/programs/entities/program.entity';
import { Course } from 'src/courses/entities/course.entity';
import { SchoolYear } from 'src/school_year/entities/school_year.entity';

@Entity('program_year_courses')
export class ProgramYearCourse {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ type: 'int', nullable: false })
  program_id: number;

  @Column({ type: 'int', nullable: false })
  course_id: number;

  @Column({ type: 'int', nullable: false })
  year_level: number; // 1, 2, 3, 4

  @Column({ type: 'int', nullable: false })
  school_year_id: number;

  @CreateDateColumn({ type: 'timestamp' })
  created_at: Date;

  @UpdateDateColumn({ type: 'timestamp' })
  updated_at: Date;

  @ManyToOne(() => Program, { onDelete: 'CASCADE' })
  @JoinColumn({ name: 'program_id' })
  program: Program;

  @ManyToOne(() => Course, { onDelete: 'CASCADE' })
  @JoinColumn({ name: 'course_id' })
  course: Course;

  @ManyToOne(() => SchoolYear, { onDelete: 'CASCADE' })
  @JoinColumn({ name: 'school_year_id' })
  schoolYear: SchoolYear;
}
