import { Entity, PrimaryGeneratedColumn, ManyToOne, JoinColumn } from 'typeorm';
import { User_Accounts } from 'src/user/entities/user.entity';
import { Course } from 'src/courses/entities/course.entity';

@Entity('user_expertise')
export class UserExpertise {
  @PrimaryGeneratedColumn()
  id: number;

  @ManyToOne(() => User_Accounts, (user) => user.expertise, {
    onDelete: 'CASCADE',
  })
  @JoinColumn({ name: 'user_id' })
  user: User_Accounts;

  @ManyToOne(() => Course, { eager: true, onDelete: 'CASCADE' })
  @JoinColumn({ name: 'course_id' })
  course: Course;
}
