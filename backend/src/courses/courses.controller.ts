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

import { CoursesService } from './courses.service';
import { CreateCourseDto } from './dto/create-course.dto';
import { UpdateCourseDto } from './dto/update-course.dto';

@Controller('courses')
export class CoursesController {
  constructor(private readonly coursesService: CoursesService) {}

  // 🔹 BULK INSERT
  @Post('add-courses')
  create(@Body() createCourseDto: CreateCourseDto[]) {
    return this.coursesService.createMany(createCourseDto);
  }

  @Get('get-courses')
  findAll() {
    return this.coursesService.findAll();
  }

  @Get('get-report-curriculum-offer')
  findReportCurriculum() {
    return this.coursesService.findReportCurriculum();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.coursesService.findOne(+id);
  }

  @Patch('update-course/:id')
  update(@Param('id') id: string, @Body() updateCourseDto: UpdateCourseDto) {
    return this.coursesService.update(+id, updateCourseDto);
  }

  @Delete('delete-id/:id')
  remove(@Param('id') id: string) {
    const numericId = parseInt(id, 10);

    if (isNaN(numericId)) {
      throw new BadRequestException('Invalid course ID');
    }

    return this.coursesService.remove(numericId);
  }
}
