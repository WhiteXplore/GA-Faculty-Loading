// school_year.entity.ts
import { Entity, Column, PrimaryGeneratedColumn, Unique } from 'typeorm';

@Entity('school_years')
@Unique(['school_year_name', 'semester']) // <- include semester
export class SchoolYear {
  @PrimaryGeneratedColumn()
  school_year_id: number;

  @Column()
  school_year_name: string;

  @Column()
  start_year: number;

  @Column()
  end_year: number;

  @Column()
  semester: number;

  @Column({ default: false })
  is_active: boolean;

  @Column({ type: 'timestamp', default: () => 'CURRENT_TIMESTAMP' })
  created_at: Date;

  @Column({ type: 'timestamp', default: () => 'CURRENT_TIMESTAMP' })
  updated_at: Date;
}
