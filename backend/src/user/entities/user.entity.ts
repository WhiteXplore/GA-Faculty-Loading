import {
  Entity,
  Column,
  PrimaryGeneratedColumn,
  ManyToOne,
  OneToMany,
  JoinColumn,
} from 'typeorm';
import { Institute } from 'src/institute/entities/institute.entity';
import { Program } from 'src/programs/entities/program.entity';
import { UserExpertise } from 'src/user/entities/user_expertise.entity';
import { UserOtherExpertise } from 'src/user/entities/user_other_expertise.entity';
import { SchoolYear } from 'src/school_year/entities/school_year.entity';
import { FacultyBranch } from 'src/faculty_branch/entities/faculty_branch.entity';
@Entity('user_accounts')
export class User_Accounts {
  @PrimaryGeneratedColumn('increment')
  id: number;

  @Column()
  first_name: string;

  @Column()
  last_name: string;

  @Column()
  email: string;

  @Column()
  password: string;

  @Column()
  role: string;

  @Column()
  employment_type: string;

  @Column()
  unit_load: number;

  @Column()
  designation: string;

  @Column({ nullable: true })
  preffered_time: string;

  // Institute Relationship
  @ManyToOne(() => Institute, (institute) => institute.users, {
    onDelete: 'CASCADE',
  })
  @JoinColumn({ name: 'institute_id' })
  institute: Institute;

  // Program Relationship
  @ManyToOne(() => Program, (program) => program.users, {
    onDelete: 'CASCADE',
  })
  @JoinColumn({ name: 'program_id' })
  program: Program;

  // School Year Relationship ✅
  @ManyToOne(() => SchoolYear, {
    onDelete: 'SET NULL',
    eager: true,
  })
  @JoinColumn({ name: 'school_year_id' })
  school_year: SchoolYear;

  // Expertise Relationships
  @OneToMany(() => UserExpertise, (expertise) => expertise.user, {
    cascade: true,
  })
  expertise: UserExpertise[];

  @OneToMany(() => UserOtherExpertise, (other) => other.user, {
    cascade: true,
  })
  other_expertise: UserOtherExpertise[];

  @OneToMany(() => FacultyBranch, (fb) => fb.user, {
    cascade: true,
  })
  facultyBranches: FacultyBranch[];
}
