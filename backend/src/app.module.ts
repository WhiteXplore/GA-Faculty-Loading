import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { AuthModule } from './auth/auth.module';
import { UserModule } from './user/user.module';
import { HttpModule } from '@nestjs/axios';
import { InstructorsModule } from './instructors/instructors.module';
import { CoursesModule } from './courses/courses.module';
import { CurriculumModule } from './curriculum/curriculum.module';
import { ProgramsModule } from './programs/programs.module';
import { RoomsModule } from './rooms/rooms.module';
import { InstituteModule } from './institute/institute.module';
import { CalendarModule } from './calendar/calendar.module';
import { AssignClassModule } from './assign_class/assign_class.module';
import { GeneratedScheduledModule } from './generated_scheduled/generated_scheduled.module';
import { ActiveYearModule } from './active_year/active_year.module';
import { ActiveSemModule } from './active_sem/active_sem.module';
import { SelectedYearSemModule } from './selected-year-sem/selected-year-sem.module';

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
    InstructorsModule,
    CoursesModule,
    CurriculumModule,
    ProgramsModule,
    RoomsModule,
    InstituteModule,
    CalendarModule,
    AssignClassModule,
    GeneratedScheduledModule,
    ActiveYearModule,
    ActiveSemModule,
    SelectedYearSemModule,
  ],
})
export class AppModule {}
