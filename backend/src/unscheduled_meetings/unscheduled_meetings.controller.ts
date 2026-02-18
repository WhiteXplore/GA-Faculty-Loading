import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
} from '@nestjs/common';
import { UnscheduledMeetingsService } from './unscheduled_meetings.service';
import { CreateUnscheduledMeetingDto } from './dto/create-unscheduled_meeting.dto';
import { UpdateUnscheduledMeetingDto } from './dto/update-unscheduled_meeting.dto';

@Controller('unscheduled-meetings')
export class UnscheduledMeetingsController {
  constructor(
    private readonly unscheduledMeetingsService: UnscheduledMeetingsService,
  ) {}

  @Post('add-unscheduled-meetings')
  create(@Body() data: CreateUnscheduledMeetingDto[]) {
    return this.unscheduledMeetingsService.create(data);
  }

  @Get('get-all-unscheduled-meetings')
  findAll() {
    return this.unscheduledMeetingsService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.unscheduledMeetingsService.findOne(+id);
  }

  @Patch(':id')
  update(
    @Param('id') id: string,
    @Body() updateUnscheduledMeetingDto: UpdateUnscheduledMeetingDto,
  ) {
    return this.unscheduledMeetingsService.update(
      +id,
      updateUnscheduledMeetingDto,
    );
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.unscheduledMeetingsService.remove(+id);
  }
}
