import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { SelectedYearSemService } from './selected-year-sem.service';
import { SelectedYearSemController } from './selected-year-sem.controller';
import { SelectedYearSem } from './entities/selected-year-sem.entity';

@Module({
  imports: [TypeOrmModule.forFeature([SelectedYearSem])],
  controllers: [SelectedYearSemController],
  providers: [SelectedYearSemService],
})
export class SelectedYearSemModule {}
