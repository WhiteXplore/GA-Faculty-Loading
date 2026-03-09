import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  ManyToOne,
  JoinColumn,
  OneToMany,
} from 'typeorm';
import { Curriculum } from 'src/curriculum/entities/curriculum.entity';
import { AssignClass } from 'src/assign_class/entities/assign_class.entity';
@Entity('courses')
export class Course {
  @PrimaryGeneratedColumn()
  course_id: number;

  @Column({ type: 'int', nullable: true })
  curriculum_id: number;

  @Column({ type: 'varchar', length: 100 })
  course_code: string;

  // @Column({ type: 'varchar', length: 255 })
  // course_description: string;

  @Column({ type: 'varchar', length: 255 })
  course_title: string;

  @Column({ type: 'int' })
  course_semester: number;

  @Column({ type: 'int' })
  course_level: number;

  @Column({ type: 'int' })
  course_lec: number;

  @Column({ type: 'int' })
  course_lab: number;

  @Column({ type: 'varchar', length: 255, nullable: true })
  course_requisite: string;

  @CreateDateColumn({ type: 'timestamp' })
  created_at: Date;

  @UpdateDateColumn({ type: 'timestamp' })
  update_at: Date;

  // @ManyToOne(() => Curriculum, (curriculum) => curriculum.courses, {
  //   onDelete: 'SET NULL',
  // })
  // @JoinColumn({ name: 'curriculum_id' })
  // curriculum: Curriculum;

  @OneToMany(() => AssignClass, (assignClass) => assignClass.course)
  assignClasses: AssignClass[];
}
