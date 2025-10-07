import { Module } from '@nestjs/common';
import { InstructorsService } from './instructors.service';
import { InstructorsController } from './instructors.controller';
import { Instructor } from './entities/instructor.entity';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Program } from 'src/programs/entities/program.entity';
import { Institute } from 'src/institute/entities/institute.entity';
import { InstructorExpertise } from './entities/instructor_expertise.entity';
@Module({
  imports: [
    TypeOrmModule.forFeature([
      Instructor,
      Program,
      Institute,
      InstructorExpertise,
    ]),
  ],
  controllers: [InstructorsController],
  providers: [InstructorsService],
})
export class InstructorsModule {}
