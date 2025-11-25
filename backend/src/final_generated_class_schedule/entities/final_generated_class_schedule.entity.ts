import { Entity, Column, PrimaryGeneratedColumn } from 'typeorm';

@Entity('final_generated_class_schedule')
export class FinalGeneratedClassSchedule {
  @PrimaryGeneratedColumn()
  id: number; // internal DB ID

  @Column({ type: 'int', nullable: true })
  class_id: number;

  @Column({ type: 'varchar', length: 255, nullable: true })
  course_code: string;

  @Column({ type: 'int', nullable: true })
  program_id: number;

  @Column({ type: 'int', nullable: true })
  institute_id: number;

  @Column({ type: 'varchar', length: 50, nullable: true })
  type: string; // Lecture, Lab, etc.

  @Column({ type: 'varchar', length: 50, nullable: true })
  day: string; // e.g., Monday

  @Column({ type: 'int', nullable: true })
  start_hour: number; // 24-hour format

  @Column({ type: 'int', nullable: true })
  duration: number;

  @Column({ type: 'varchar', length: 50, nullable: true })
  time_slot: string; // e.g., "8:00 AM - 11:00 AM"

  @Column({ type: 'int', nullable: true })
  room_id: number;

  @Column({ type: 'varchar', length: 100, nullable: true })
  room_name: string;

  @Column({ type: 'varchar', length: 50, nullable: true })
  room_type: string;

  @Column({ type: 'int', nullable: true })
  room_capacity: number;

  @Column({ type: 'int', nullable: true })
  class_size: number;

  @Column({ type: 'int', nullable: true })
  faculty_id: number;

  @Column({ type: 'varchar', length: 255, nullable: true })
  faculty_name: string;

  @Column({ type: 'varchar', length: 10, nullable: true })
  school_year: string;

  @Column({ type: 'varchar', length: 10, nullable: true })
  semester: string;
}
