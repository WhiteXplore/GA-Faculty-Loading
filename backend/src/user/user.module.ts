import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { UserService } from './user.service';
import { UserController } from './user.controller';
import { User_Accounts } from './entities/user.entity';
import { UserExpertise } from './entities/user_expertise.entity';
import { UserOtherExpertise } from './entities/user_other_expertise.entity';
import { Program } from 'src/programs/entities/program.entity';
import { Course } from 'src/courses/entities/course.entity';
UserOtherExpertise;
@Module({
  imports: [
    TypeOrmModule.forFeature([
      User_Accounts,
      UserExpertise,
      UserOtherExpertise,
      Program,
      Course,
    ]),
  ],
  controllers: [UserController],
  providers: [UserService],
})
export class UserModule {}
