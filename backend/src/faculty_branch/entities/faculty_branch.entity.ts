import {
  Entity,
  Column,
  PrimaryGeneratedColumn,
  ManyToOne,
  OneToMany,
  JoinColumn,
} from 'typeorm';
import { User_Accounts } from 'src/user/entities/user.entity';
import { CollegeBranch } from 'src/college_branch/entities/college_branch.entity';

@Entity('faculty_branch')
export class FacultyBranch {
  @PrimaryGeneratedColumn('increment')
  faculty_branch_id: number;

  // Many FacultyBranch rows → One User
  @ManyToOne(() => User_Accounts, (user) => user.facultyBranches, {
    onDelete: 'CASCADE',
  })
  @JoinColumn({ name: 'user_id' })
  user: User_Accounts;

  // Many FacultyBranch rows → One CollegeBranch
  @ManyToOne(() => CollegeBranch, (branch) => branch.facultyBranches, {
    onDelete: 'CASCADE',
  })
  @JoinColumn({ name: 'college_branch_id' })
  collegeBranch: CollegeBranch;
}
