import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
} from 'typeorm';

@Entity('school_years')
export class SchoolYear {
  @PrimaryGeneratedColumn()
  school_year_id: number;

  @Column({ type: 'varchar', length: 50, unique: true })
  school_year_name: string;

  @Column({ type: 'int' })
  start_year: number;

  @Column({ type: 'int' })
  end_year: number;

  @Column({ type: 'boolean', default: false })
  is_active: boolean;

  @CreateDateColumn({ type: 'timestamp' })
  created_at: Date;

  @UpdateDateColumn({ type: 'timestamp' })
  updated_at: Date;
}

