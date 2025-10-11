import { Entity, PrimaryGeneratedColumn, Column } from 'typeorm';

@Entity('active_sem')
export class ActiveSem {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({
    type: 'int',
    default: 1,
    comment: '1 = 1st Semester, 2 = 2nd Semester, 3 = Summer',
  })
  semester: number;

  @Column({ type: 'boolean', default: true })
  is_active: boolean;
}
