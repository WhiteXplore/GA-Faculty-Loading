import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { ProgramYearCoursesService } from './program_year_courses.service';
import { ProgramYearCoursesController } from './program_year_courses.controller';
import { ProgramYearCourse } from './entities/program_year_course.entity';

@Module({
  imports: [TypeOrmModule.forFeature([ProgramYearCourse])],
  controllers: [ProgramYearCoursesController],
  providers: [ProgramYearCoursesService],
  exports: [ProgramYearCoursesService],
})
export class ProgramYearCoursesModule {}








