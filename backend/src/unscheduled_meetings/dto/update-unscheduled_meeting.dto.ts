import { PartialType } from '@nestjs/mapped-types';
import { CreateUnscheduledMeetingDto } from './create-unscheduled_meeting.dto';

export class UpdateUnscheduledMeetingDto extends PartialType(
  CreateUnscheduledMeetingDto,
) {}
