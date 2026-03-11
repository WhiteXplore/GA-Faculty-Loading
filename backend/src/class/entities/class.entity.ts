import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  ManyToOne,
  JoinColumn,
} from 'typeorm';
import { SchoolYear } from 'src/school_year/entities/school_year.entity';
import { Program } from 'src/programs/entities/program.entity';
import { CollegeBranch } from 'src/college_branch/entities/college_branch.entity';

@Entity('classes')
export class Class {
  @PrimaryGeneratedColumn()
  class_id: number;

  @Column({ type: 'int', nullable: false })
  school_year_id: number;

  @Column({ type: 'int', nullable: false })
  program_id: number;

  @Column({ type: 'int', nullable: true })
  college_branch_id: number;

  @Column({ type: 'varchar', length: 100 })
  set_name: string;

  @Column({ type: 'int' })
  class_size: number;

  @CreateDateColumn({ type: 'timestamp' })
  created_at: Date;

  @UpdateDateColumn({ type: 'timestamp' })
  updated_at: Date;

  @ManyToOne(() => SchoolYear, { onDelete: 'CASCADE' })
  @JoinColumn({ name: 'school_year_id' })
  schoolYear: SchoolYear;

  @ManyToOne(() => Program, { onDelete: 'CASCADE' })
  @JoinColumn({ name: 'program_id' })
  program: Program;

  @ManyToOne(() => CollegeBranch, { onDelete: 'CASCADE' })
  @JoinColumn({ name: 'college_branch_id' })
  colleges: CollegeBranch;
}
