import { Module } from '@nestjs/common';
import { SchoolYearService } from './school_year.service';
import { SchoolYearController } from './school_year.controller';
import { TypeOrmModule } from '@nestjs/typeorm';
import { SchoolYear } from './entities/school_year.entity';

@Module({
  imports: [TypeOrmModule.forFeature([SchoolYear])],
  controllers: [SchoolYearController],
  providers: [SchoolYearService],
})
export class SchoolYearModule {}

