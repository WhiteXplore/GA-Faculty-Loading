import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  ManyToOne,
  JoinColumn,
} from 'typeorm';
import { Program } from 'src/programs/entities/program.entity';
import { Course } from 'src/courses/entities/course.entity';

@Entity('assign_class')
export class AssignClass {
  @PrimaryGeneratedColumn()
  assign_class_id: number;

  @ManyToOne(() => Program, (program) => program.assignClasses, { eager: true })
  @JoinColumn({ name: 'program_id' })
  program: Program;

  @Column()
  program_id: number;

  @ManyToOne(() => Course, (course) => course.assignClasses, { eager: true })
  @JoinColumn({ name: 'course_id' })
  course: Course;

  @Column()
  course_id: number;

  @Column({ length: 5 })
  set: string;
}
