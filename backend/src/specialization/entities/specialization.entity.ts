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

@Entity('specializations')
export class Specialization {
  @PrimaryGeneratedColumn()
  specialization_id: number;

  @Column({ type: 'int', nullable: false })
  program_id: number;

  @Column({ type: 'varchar', length: 255 })
  specialization_name: string;

  @CreateDateColumn({ type: 'timestamp' })
  created_at: Date;

  @UpdateDateColumn({ type: 'timestamp' })
  updated_at: Date;

  @ManyToOne(() => Program, { onDelete: 'CASCADE' })
  @JoinColumn({ name: 'program_id' })
  program: Program;
}

