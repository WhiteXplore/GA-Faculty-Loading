import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  ManyToOne,
  OneToMany,
  JoinColumn,
} from 'typeorm';
import { CollegeBranch } from 'src/college_branch/entities/college_branch.entity';
import { BuildingArea } from 'src/building_areas/entities/building_area.entity';
import { Room } from 'src/rooms/entities/room.entity';
@Entity('buildings')
export class Building {
  @PrimaryGeneratedColumn()
  building_id: number;

  @Column({ type: 'varchar', length: 150 })
  building_name: string;

  //   Relationship to CollegeBranch

  @ManyToOne(() => CollegeBranch, (branch) => branch.buildings, {
    onDelete: 'RESTRICT',
    nullable: true,
  })
  @JoinColumn({ name: 'college_branch_id' })
  collegeBranch: CollegeBranch;

  //   Relationship to BuildingArea

  @ManyToOne(() => BuildingArea, (area) => area.buildings, {
    onDelete: 'RESTRICT',
    nullable: true,
  })
  @JoinColumn({ name: 'building_area_id' })
  buildingArea: BuildingArea;

  @OneToMany(() => Room, (rm) => rm.building)
  rooms: Room[];
}
