import { Entity, PrimaryGeneratedColumn, Column, OneToMany } from 'typeorm';
import { Class } from 'src/class/entities/class.entity';
import { Room } from 'src/rooms/entities/room.entity';
@Entity('college_branch')
export class CollegeBranch {
  @PrimaryGeneratedColumn()
  college_branch_id: number;

  @Column({ type: 'varchar', length: 100 })
  college_branch_name: string;

  @OneToMany(() => Class, (cls) => cls.colleges)
  classes: Class[];

  @OneToMany(() => Room, (rm) => rm.collegeBranch)
  rooms: Room[];
}
