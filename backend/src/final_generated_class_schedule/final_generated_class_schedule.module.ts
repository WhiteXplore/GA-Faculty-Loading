import { Module } from '@nestjs/common';
import { FinalGeneratedClassScheduleService } from './final_generated_class_schedule.service';
import { FinalGeneratedClassScheduleController } from './final_generated_class_schedule.controller';
import { TypeOrmModule } from '@nestjs/typeorm';
import { FinalGeneratedClassSchedule } from './entities/final_generated_class_schedule.entity';
@Module({
  imports: [TypeOrmModule.forFeature([FinalGeneratedClassSchedule])],
  controllers: [FinalGeneratedClassScheduleController],
  providers: [FinalGeneratedClassScheduleService],
})
export class FinalGeneratedClassScheduleModule {}
