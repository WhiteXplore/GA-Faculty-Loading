import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  ManyToOne,
  JoinColumn,
} from 'typeorm';
import { Instructor } from './instructor.entity';
import { Exclude } from 'class-transformer';

@Entity('instructor_expertise')
export class InstructorExpertise {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  expertise: string;

  @Column()
  instructor_id: number;

  @ManyToOne(() => Instructor, (instructor) => instructor.expertise, {
    onDelete: 'CASCADE',
  })
  @JoinColumn({ name: 'instructor_id' })
  @Exclude() // prevents circular reference when sending JSON
  instructor: Instructor;
}
