import { Module } from '@nestjs/common';
import { GeneratedScheduledService } from './generated_scheduled.service';
import { GeneratedScheduledController } from './generated_scheduled.controller';

@Module({
  controllers: [GeneratedScheduledController],
  providers: [GeneratedScheduledService],
})
export class GeneratedScheduledModule {}
