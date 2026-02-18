import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';

import { UnscheduledMeetingsController } from './unscheduled_meetings.controller';
import { UnscheduledMeeting } from './entities/unscheduled_meeting.entity';
import { UnscheduledMeetingsService } from './unscheduled_meetings.service';

@Module({
  imports: [TypeOrmModule.forFeature([UnscheduledMeeting])],
  controllers: [UnscheduledMeetingsController],
  providers: [UnscheduledMeetingsService],
})
export class UnscheduledMeetingsModule {}
