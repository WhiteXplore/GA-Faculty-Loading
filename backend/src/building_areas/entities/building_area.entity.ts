import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  OneToMany,
  JoinColumn,
} from 'typeorm';
import { Building } from 'src/buildings/entities/building.entity';
@Entity('building_areas')
export class BuildingArea {
  @PrimaryGeneratedColumn()
  building_area_id: number;

  @Column({ type: 'varchar', length: 150 })
  area_name: string;

  @Column({ type: 'int', nullable: true })
  time_travel: number;

  @OneToMany(() => Building, (bldg) => bldg.buildingArea)
  buildings: Building[];
}
