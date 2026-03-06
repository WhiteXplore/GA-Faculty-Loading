import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  OneToMany,
  ManyToOne,
  JoinColumn,
} from 'typeorm';
import { Program } from 'src/programs/entities/program.entity';
import { Course } from 'src/courses/entities/course.entity';
import { Institute } from 'src/institute/entities/institute.entity';

@Entity('curricula')
export class Curriculum {
  @PrimaryGeneratedColumn()
  curriculum_id: number;

  @Column({ type: 'int' })
  institute_id: number;

  @Column({ type: 'int' })
  program_id: number;

  @Column({ type: 'int' })
  curriculum_start_year: number;

  @Column({ type: 'int' })
  curriculum_end_year: number;

  @CreateDateColumn({ type: 'timestamp' })
  created_at: Date;

  @UpdateDateColumn({ type: 'timestamp' })
  updated_at: Date;

  // 🔹 Relations
  @ManyToOne(() => Institute, (institute) => institute.programs, {
    onDelete: 'CASCADE',
  })
  @JoinColumn({ name: 'institute_id' })
  institute: Institute;

  @ManyToOne(() => Program, (program) => program.curricula, {
    onDelete: 'RESTRICT',
  })
  @JoinColumn({ name: 'program_id' })
  program: Program;

  @OneToMany(() => Course, (course) => course.curriculum)
  courses: Course[];
}
