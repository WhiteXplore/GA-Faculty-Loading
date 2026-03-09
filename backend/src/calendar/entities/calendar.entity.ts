// src/calendar/entities/calendar.entity.ts
import {
  Entity,
  Column,
  PrimaryGeneratedColumn,
  ManyToOne,
  JoinColumn,
} from 'typeorm';
import { Program } from 'src/programs/entities/program.entity';

@Entity('calendar')
export class Calendar {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  title: string;

  @Column({ type: 'date' })
  startDate: string;

  @Column({ type: 'date' })
  endDate: string;

  @Column({ type: 'time', nullable: true })
  timeStart: string;

  @Column({ type: 'time', nullable: true })
  timeEnd: string;

  @Column({ type: 'boolean', default: false })
  isAllDay: boolean;

  // 🔽 Foreign key column
  @Column({ type: 'int', nullable: true })
  program_id: number;

  // 🔽 Relationship to Program
  @ManyToOne(() => Program, (program) => program.calendarEvents, {
    nullable: true,
    onDelete: 'SET NULL',
  })
  @JoinColumn({ name: 'program_id' })
  program: Program;
}
