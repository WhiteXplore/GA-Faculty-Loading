import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
  BadRequestException,
} from '@nestjs/common';
import { SchoolYearService } from './school_year.service';
import { CreateSchoolYearDto } from './dto/create-school_year.dto';
import { UpdateSchoolYearDto } from './dto/update-school_year.dto';

@Controller('school-year')
export class SchoolYearController {
  constructor(private readonly schoolYearService: SchoolYearService) {}

  @Post('add-school-year')
  create(@Body() createSchoolYearDto: CreateSchoolYearDto) {
    return this.schoolYearService.create(createSchoolYearDto);
  }
  // school_year.controller.ts
  @Get('latest-active')
  getLatestActive() {
    return this.schoolYearService.findLatestActive();
  }

  @Get('get-school-years')
  findAll() {
    return this.schoolYearService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.schoolYearService.findOne(+id);
  }
  @Patch('update-timestamp/:id')
  async updateTimestamp(@Param('id') id: number) {
    return this.schoolYearService.updateTimestamp(id);
  }

  @Patch('update-school-year/:id')
  update(
    @Param('id') id: string,
    @Body() updateSchoolYearDto: UpdateSchoolYearDto,
  ) {
    return this.schoolYearService.update(+id, updateSchoolYearDto);
  }

  @Delete('delete-id/:id')
  remove(@Param('id') id: string) {
    const numericId = parseInt(id, 10);
    if (isNaN(numericId)) {
      throw new BadRequestException('Invalid school year ID');
    }
    return this.schoolYearService.remove(numericId);
  }
}
