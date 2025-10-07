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

  @ManyToOne(() => Institute, (institute) => institute.users, {
    onDelete: 'CASCADE',
  })
  @JoinColumn({ name: 'institute_id' })
  institute: Institute;

  @ManyToOne(() => Program, (program) => program.users, {
    onDelete: 'CASCADE',
  })
  @JoinColumn({ name: 'program_id' })
  program: Program;

  @OneToMany(() => UserExpertise, (expertise) => expertise.user, {
    cascade: true,
  })
  expertise: UserExpertise[];

  @OneToMany(() => UserOtherExpertise, (other) => other.user, {
    cascade: true,
  })
  other_expertise: UserOtherExpertise[];
}
