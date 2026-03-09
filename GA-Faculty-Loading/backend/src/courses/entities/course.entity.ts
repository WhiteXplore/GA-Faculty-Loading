import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  ManyToOne,
  JoinColumn,
  OneToMany,
} from 'typeorm';
import { Curriculum } from 'src/curriculum/entities/curriculum.entity';
import { AssignClass } from 'src/assign_class/entities/assign_class.entity';
import { Institute } from 'src/institute/entities/institute.entity';
import { Program } from 'src/programs/entities/program.entity';

@Entity('courses')
export class Course {
  @PrimaryGeneratedColumn()
  course_id: number;

  @Column({ type: 'varchar', length: 100 })
  course_code: string;

  @Column({ type: 'varchar', length: 255 })
  course_title: string;

  @Column({ type: 'int' })
  course_semester: number;

  @Column({ type: 'int' })
  course_level: number;

  @Column({ type: 'int' })
  course_lec: number;

  @Column({ type: 'int' })
  course_lab: number;

  @Column({ type: 'varchar', length: 255, nullable: true })
  course_requisite: string;

  // 🔹 Relationships
  @ManyToOne(() => Institute, { onDelete: 'SET NULL' })
  @JoinColumn({ name: 'institute_id' })
  institute: Institute;

  @Column({ type: 'int', nullable: true })
  institute_id: number;

  @ManyToOne(() => Program, (program) => program.courses, {
    onDelete: 'SET NULL',
  })
  @JoinColumn({ name: 'program_id' })
  program: Program;

  @Column({ type: 'int', nullable: true })
  program_id: number;

  @ManyToOne(() => Curriculum, (curriculum) => curriculum.courses, {
    onDelete: 'SET NULL',
  })
  @JoinColumn({ name: 'curriculum_id' })
  curriculum: Curriculum;

  @Column({ type: 'int', nullable: true })
  curriculum_id: number;

  @OneToMany(() => AssignClass, (assignClass) => assignClass.course)
  assignClasses: AssignClass[];

  @CreateDateColumn({ type: 'timestamp' })
  created_at: Date;

  @UpdateDateColumn({ type: 'timestamp' })
  update_at: Date;
}
