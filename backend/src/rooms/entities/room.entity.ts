import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  ManyToOne,
  JoinColumn,
} from 'typeorm';
import { Institute } from 'src/institute/entities/institute.entity';

@Entity('rooms')
export class Room {
  @PrimaryGeneratedColumn()
  room_id: number;

  @Column({ type: 'int', nullable: true })
  institute_id: number;

  @Column({ type: 'varchar', length: 150 })
  building_name: string;

  @Column({ type: 'varchar', length: 50 })
  level: string;

  @Column({ type: 'varchar', length: 100 })
  room_name: string;

  @Column({ type: 'int' })
  room_capacity: number;

  @Column({ type: 'varchar', length: 100 })
  room_type: string;

  @CreateDateColumn({ type: 'timestamp' })
  created_at: Date;

  @UpdateDateColumn({ type: 'timestamp' })
  updated_at: Date;

  @ManyToOne(() => Institute, (institute) => institute.rooms, {
    onDelete: 'RESTRICT',
    nullable: true,
  })
  @JoinColumn({ name: 'institute_id' })
  institute: Institute;
}
