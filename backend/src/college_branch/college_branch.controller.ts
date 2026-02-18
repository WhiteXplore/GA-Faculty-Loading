import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
} from '@nestjs/common';
import { CollegeBranchService } from './college_branch.service';
import { CreateCollegeBranchDto } from './dto/create-college_branch.dto';
import { UpdateCollegeBranchDto } from './dto/update-college_branch.dto';

@Controller('college-branch')
export class CollegeBranchController {
  constructor(private readonly collegeBranchService: CollegeBranchService) {}

  @Post('add-college-branch')
  create(@Body() createCollegeBranchDto: CreateCollegeBranchDto) {
    return this.collegeBranchService.create(createCollegeBranchDto);
  }

  @Get('get-college-branch')
  findAll() {
    return this.collegeBranchService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.collegeBranchService.findOne(+id);
  }

  @Patch(':id')
  update(
    @Param('id') id: string,
    @Body() updateCollegeBranchDto: UpdateCollegeBranchDto,
  ) {
    return this.collegeBranchService.update(+id, updateCollegeBranchDto);
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.collegeBranchService.remove(+id);
  }
}
