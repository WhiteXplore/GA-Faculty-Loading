import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
} from '@nestjs/common';

import { GeneratedScheduledService } from './generated_scheduled.service';
import { CreateGeneratedScheduledDto } from './dto/create-generated_scheduled.dto';
import { UpdateGeneratedScheduledDto } from './dto/update-generated_scheduled.dto';

@Controller('generated-scheduled')
export class GeneratedScheduledController {
  constructor(
    private readonly generatedScheduledService: GeneratedScheduledService,
  ) {}

  @Post()
  create(@Body() createGeneratedScheduledDto: CreateGeneratedScheduledDto) {
    return this.generatedScheduledService.create(createGeneratedScheduledDto);
  }

  /**
   * ⭐ Run Python Scheduler
   */
  @Get('load')
  async runScheduler() {
    const data =
      await this.generatedScheduledService.runPythonScheduler();

    return {
      success: true,
      data,
    };
  }

  /**
   * ⭐ Read JSON output
   */
  @Get('generate')
  getGeneratedSchedule() {
    const data =
      this.generatedScheduledService.getFacultyLoadingFromFile();

    return {
      success: true,
      data,
    };
  }

  @Get()
  findAll() {
    return this.generatedScheduledService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.generatedScheduledService.findOne(+id);
  }

  @Patch(':id')
  update(
    @Param('id') id: string,
    @Body() updateGeneratedScheduledDto: UpdateGeneratedScheduledDto,
  ) {
    return this.generatedScheduledService.update(
      +id,
      updateGeneratedScheduledDto,
    );
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.generatedScheduledService.remove(+id);
  }
}