import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  ManyToOne,
  OneToMany,
  JoinColumn,
} from 'typeorm';

import { BuildingArea } from 'src/building_areas/entities/building_area.entity';
import { Room } from 'src/rooms/entities/room.entity';

@Entity('buildings')
export class Building {
  @PrimaryGeneratedColumn()
  building_id: number;

  @Column({ type: 'varchar', length: 150 })
  building_name: string;

  @ManyToOne(() => BuildingArea, (area) => area.buildings, {
    onDelete: 'RESTRICT',
    nullable: true,
  })
  @JoinColumn({ name: 'building_area_id' })
  buildingArea: BuildingArea;

  @OneToMany(() => Room, (rm) => rm.building)
  rooms: Room[];
}
