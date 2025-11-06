import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
  Query,
} from '@nestjs/common';
import { ProgramYearCoursesService } from './program_year_courses.service';
import { CreateProgramYearCourseDto } from './dto/create-program_year_course.dto';
import { UpdateProgramYearCourseDto } from './dto/update-program_year_course.dto';

@Controller('program-year-courses')
export class ProgramYearCoursesController {
  constructor(
    private readonly programYearCoursesService: ProgramYearCoursesService,
  ) {}

  @Post('create')
  create(@Body() createDto: CreateProgramYearCourseDto) {
    return this.programYearCoursesService.create(createDto);
  }

  @Post('create-bulk')
  createBulk(@Body() createDtos: CreateProgramYearCourseDto[]) {
    return this.programYearCoursesService.createBulk(createDtos);
  }

  @Get('get-all')
  findAll() {
    return this.programYearCoursesService.findAll();
  }

  @Get('view-all')
  findFromView() {
    return this.programYearCoursesService.findFromView();
  }

  @Get('get-by-program-and-school-year')
  findByProgramAndSchoolYear(
    @Query('program_id') programId: number,
    @Query('school_year_id') schoolYearId: number,
  ) {
    return this.programYearCoursesService.findByProgramAndSchoolYear(
      programId,
      schoolYearId,
    );
  }

  @Get('get-by-year-level')
  findByProgramYearLevelAndSchoolYear(
    @Query('program_id') programId: number,
    @Query('year_level') yearLevel: number,
    @Query('school_year_id') schoolYearId: number,
  ) {
    return this.programYearCoursesService.findByProgramYearLevelAndSchoolYear(
      programId,
      yearLevel,
      schoolYearId,
    );
  }

  @Get('get-one/:id')
  findOne(@Param('id') id: string) {
    return this.programYearCoursesService.findOne(+id);
  }

  @Patch('update/:id')
  update(
    @Param('id') id: string,
    @Body() updateDto: UpdateProgramYearCourseDto,
  ) {
    return this.programYearCoursesService.update(+id, updateDto);
  }

  @Delete('delete/:id')
  remove(@Param('id') id: string) {
    return this.programYearCoursesService.remove(+id);
  }

  @Delete('delete-by-year-level')
  removeByProgramYearLevelAndSchoolYear(
    @Query('program_id') programId: number,
    @Query('year_level') yearLevel: number,
    @Query('school_year_id') schoolYearId: number,
  ) {
    return this.programYearCoursesService.removeByProgramYearLevelAndSchoolYear(
      programId,
      yearLevel,
      schoolYearId,
    );
  }

  @Post('sync-from-classes')
  async syncFromClasses() {
    await this.programYearCoursesService.syncProgramYearCoursesFromClasses();
    return {
      message: 'Program year courses synced successfully from classes.',
    };
  }
}
