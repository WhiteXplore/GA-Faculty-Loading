import { Entity, Column, PrimaryGeneratedColumn } from 'typeorm';

@Entity('final_generated_class_schedule')
export class FinalGeneratedClassSchedule {
  @PrimaryGeneratedColumn()
  id: number; // internal DB ID

  @Column({ type: 'int', nullable: true })
  class_id: number;

  @Column({ type: 'int', nullable: true })
  course_id: number;

  @Column({ type: 'varchar', length: 20, nullable: true })
  course_code: string;

  @Column({ type: 'varchar', length: 50, nullable: true })
  set_name: string;

  @Column({ type: 'int', nullable: true })
  program_id: number;

  @Column({ type: 'varchar', length: 50, nullable: true })
  program_code: string;

  @Column({ type: 'int', nullable: true })
  institute_id: number;

  @Column({ type: 'varchar', length: 50, nullable: true })
  type: string; // Lecture, Lab, etc.

  @Column({ type: 'varchar', length: 50, nullable: true })
  day: string; // e.g., Monday

  @Column({ type: 'float', nullable: true })
  start_hour: number; // allows 16.5, 14.25, etc.

  @Column({ type: 'float', nullable: true })
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

  @Column({ type: 'varchar', length: 20, nullable: true })
  school_year: string;

  @Column({ type: 'varchar', length: 10, nullable: true })
  semester: string;

  @Column({
    type: 'varchar',
    length: 50,
    nullable: true,
    default: 'face to face',
  })
  mode: string;

  // -------------------------
  // NEW: Join tracking fields
  // -------------------------

  @Column({ type: 'int', nullable: true })
  join_group_id: number; // all schedules in same join group share this ID

  @Column({ type: 'boolean', default: false, nullable: true })
  is_joined: boolean; // true if part of a joined set

  @Column({ type: 'simple-array', nullable: true })
  joined_with: number[]; // array of schedule IDs in the same join group
}
