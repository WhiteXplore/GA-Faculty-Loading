import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
} from '@nestjs/common';
import { InstituteService } from './institute.service';
import { CreateInstituteDto } from './dto/create-institute.dto';
import { UpdateInstituteDto } from './dto/update-institute.dto';

@Controller('institute')
export class InstituteController {
  constructor(private readonly instituteService: InstituteService) {}

  @Post('add-institute')
  async create(@Body() createInstituteDto: CreateInstituteDto) {
    return await this.instituteService.create(createInstituteDto);
  }

  @Get('get-institutes')
  async findAll() {
    return await this.instituteService.findAll();
  }

  @Get(':id')
  async findOne(@Param('id') id: string) {
    return await this.instituteService.findOne(+id);
  }

  @Patch('update-institute/:id')
  async update(
    @Param('id') id: string,
    @Body() updateInstituteDto: UpdateInstituteDto,
  ) {
    return await this.instituteService.update(+id, updateInstituteDto);
  }

  @Delete('delete-id/:id')
  async remove(@Param('id') id: string) {
    return await this.instituteService.remove(+id);
  }
}
