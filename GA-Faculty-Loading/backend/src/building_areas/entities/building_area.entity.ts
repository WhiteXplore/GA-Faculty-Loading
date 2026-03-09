import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  OneToMany,
  ManyToOne,
  JoinColumn,
} from 'typeorm';

import { Building } from 'src/buildings/entities/building.entity';
import { CollegeBranch } from 'src/college_branch/entities/college_branch.entity';

@Entity('building_areas')
export class BuildingArea {
  @PrimaryGeneratedColumn()
  building_area_id: number;

  @Column({ type: 'varchar', length: 150 })
  area_name: string;

  @Column({ type: 'int', nullable: true })
  time_travel: number;

  // MANY BuildingAreas → ONE CollegeBranch
  @ManyToOne(() => CollegeBranch, (branch) => branch.buildingAreas, {
    onDelete: 'CASCADE',
  })
  @JoinColumn({ name: 'college_branch_id' })
  collegeBranch: CollegeBranch;

  @OneToMany(() => Building, (bldg) => bldg.buildingArea)
  buildings: Building[];
}
