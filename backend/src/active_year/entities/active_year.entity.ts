import { Entity, PrimaryGeneratedColumn, Column } from 'typeorm';

@Entity()
export class ActiveYear {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ unique: true })
  year: number;

  @Column({ default: false })
  isActive: boolean;
}
