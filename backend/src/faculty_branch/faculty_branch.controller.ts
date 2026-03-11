import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
} from '@nestjs/common';
import { FacultyBranchService } from './faculty_branch.service';
import { CreateFacultyBranchDto } from './dto/create-faculty_branch.dto';
import { UpdateFacultyBranchDto } from './dto/update-faculty_branch.dto';

@Controller('faculty-branch')
export class FacultyBranchController {
  constructor(private readonly facultyBranchService: FacultyBranchService) {}

  @Post()
  create(@Body() dto: CreateFacultyBranchDto) {
    return this.facultyBranchService.create(dto);
  }

  @Get('get-all-faculty-branch')
  findAll() {
    return this.facultyBranchService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.facultyBranchService.findOne(+id);
  }

  @Patch(':id')
  update(@Param('id') id: string, @Body() dto: UpdateFacultyBranchDto) {
    return this.facultyBranchService.update(+id, dto);
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.facultyBranchService.remove(+id);
  }

  // ✅ PATCH multiple branches for a user
  @Patch('user/:user_id')
  updateBranches(
    @Param('user_id') user_id: string,
    @Body() body: { college_branch_ids: number[] },
  ) {
    return this.facultyBranchService.updateUserBranches(
      +user_id,
      body.college_branch_ids,
    );
  }
}
