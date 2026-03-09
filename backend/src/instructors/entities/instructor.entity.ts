import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  ManyToOne,
  OneToMany,
  JoinColumn,
} from 'typeorm';
import { Institute } from 'src/institute/entities/institute.entity';
import { Program } from 'src/programs/entities/program.entity';
import { InstructorExpertise } from './instructor_expertise.entity';

@Entity('instructors')
export class Instructor {
  @PrimaryGeneratedColumn()
  instructor_id: number;

  @Column({ type: 'int', nullable: true })
  institute_id: number;

  @Column({ type: 'int', nullable: true })
  program_id: number;

  @Column({ type: 'varchar', length: 255 })
  instructor_fname: string;

  @Column({ type: 'varchar', length: 255 })
  instructor_mname: string;

  @Column({ type: 'varchar', length: 255 })
  instructor_lname: string;

  @Column({ type: 'varchar', length: 50 })
  instructor_gender: string;

  @Column({ type: 'varchar', length: 100 })
  instructor_jobtype: string;

  @CreateDateColumn()
  created_at: Date;

  @UpdateDateColumn()
  updated_at: Date;

  @ManyToOne(() => Institute, (institute) => institute.instructors, {
    onDelete: 'RESTRICT',
    nullable: true,
  })
  @JoinColumn({ name: 'institute_id' })
  institute: Institute;

  @ManyToOne(() => Program, (program) => program.instructors, {
    onDelete: 'RESTRICT',
    nullable: true,
  })
  @JoinColumn({ name: 'program_id' })
  program: Program;

  @OneToMany(() => InstructorExpertise, (expertise) => expertise.instructor, {
    cascade: true,
  })
  expertise: InstructorExpertise[];
}
