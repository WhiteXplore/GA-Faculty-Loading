import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { AuthModule } from './auth/auth.module';
import { UserModule } from './user/user.module';
import { HttpModule } from '@nestjs/axios';
import { CoursesModule } from './courses/courses.module';
import { CurriculumModule } from './curriculum/curriculum.module';
import { ProgramsModule } from './programs/programs.module';
import { RoomsModule } from './rooms/rooms.module';
import { InstituteModule } from './institute/institute.module';
import { CalendarModule } from './calendar/calendar.module';
import { AssignClassModule } from './assign_class/assign_class.module';
import { GeneratedScheduledModule } from './generated_scheduled/generated_scheduled.module';
import { SchoolYearModule } from './school_year/school_year.module';
import { ClassModule } from './class/class.module';
import { ProgramYearCoursesModule } from './program_year_courses/program_year_courses.module';
import { FinalGeneratedClassScheduleModule } from './final_generated_class_schedule/final_generated_class_schedule.module';
import { CollegeBranchModule } from './college_branch/college_branch.module';
import { UnscheduledMeetingsModule } from './unscheduled_meetings/unscheduled_meetings.module';
import { FacultyBranchModule } from './faculty_branch/faculty_branch.module';
import { BuildingsModule } from './buildings/buildings.module';
import { BuildingAreasModule } from './building_areas/building_areas.module';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true, // loads .env and makes process.env available
    }),
    HttpModule,
    TypeOrmModule.forRootAsync({
      imports: [ConfigModule],
      inject: [ConfigService],
      useFactory: () => ({
        type: 'mysql',
        host: process.env.DATABASE_HOST,
        port: parseInt(process.env.DATABASE_PORT || '3306', 10),
        username: process.env.DATABASE_USER,
        password: process.env.DATABASE_PASSWORD,
        database: process.env.DATABASE_NAME,
        entities: [__dirname + '/**/*.entity{.ts,.js}'],
        synchronize: true,
      }),
    }),
    AuthModule,
    UserModule,
    CoursesModule,
    CurriculumModule,
    ProgramsModule,
    RoomsModule,
    InstituteModule,
    CalendarModule,
    AssignClassModule,
    GeneratedScheduledModule,
    SchoolYearModule,
    ClassModule,
    ProgramYearCoursesModule,
    FinalGeneratedClassScheduleModule,
    CollegeBranchModule,
    UnscheduledMeetingsModule,
    FacultyBranchModule,
    BuildingsModule,
    BuildingAreasModule,
  ],
})
export class AppModule {}
