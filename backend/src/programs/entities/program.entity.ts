import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  OneToMany,
  ManyToOne,
  JoinColumn,
} from 'typeorm';
import { Curriculum } from 'src/curriculum/entities/curriculum.entity';
import { Institute } from 'src/institute/entities/institute.entity';
import { Calendar } from 'src/calendar/entities/calendar.entity';
import { User_Accounts } from 'src/user/entities/user.entity';
import { AssignClass } from 'src/assign_class/entities/assign_class.entity';
import { Course } from 'src/courses/entities/course.entity';

@Entity('programs')
export class Program {
  @PrimaryGeneratedColumn()
  program_id: number;

  @Column({ type: 'int', nullable: true })
  institute_id: number;

  @Column({ type: 'varchar', length: 255 })
  program_name: string;

  @Column({ type: 'varchar', length: 255 })
  program_code: string;

  @CreateDateColumn({ type: 'timestamp' })
  created_at: Date;

  @UpdateDateColumn({ type: 'timestamp' })
  updated_at: Date;

  // 🔹 Relations
  @ManyToOne(() => Institute, (institute) => institute.programs, {
    onDelete: 'CASCADE',
    nullable: true,
  })
  @JoinColumn({ name: 'institute_id' })
  institute: Institute;

  @OneToMany(() => Curriculum, (curriculum) => curriculum.program)
  curricula: Curriculum[];

  @OneToMany(() => Calendar, (calendar) => calendar.program)
  calendarEvents: Calendar[];

  @OneToMany(() => User_Accounts, (user) => user.program)
  users: User_Accounts[];

  @OneToMany(() => Course, (course) => course.program)
  courses: Course[];

  @OneToMany(() => AssignClass, (assignClass) => assignClass.course)
  assignClasses: AssignClass[];
}
