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
import { Building } from 'src/buildings/entities/building.entity';
@Entity('rooms')
export class Room {
  @PrimaryGeneratedColumn()
  room_id: number;

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
  institute: Institute | null;

  @ManyToOne(() => Building, (bldg) => bldg.rooms, {
    onDelete: 'RESTRICT',
    nullable: true,
  })
  @JoinColumn({ name: 'building_id' })
  building: Building | null;
}
