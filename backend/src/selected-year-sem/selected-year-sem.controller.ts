import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
  HttpException,
  HttpStatus,
} from '@nestjs/common';
import { SelectedYearSemService } from './selected-year-sem.service';
import { CreateSelectedYearSemDto } from './dto/create-selected-year-sem.dto';
import { UpdateSelectedYearSemDto } from './dto/update-selected-year-sem.dto';

@Controller('selected-year-sem')
export class SelectedYearSemController {
  constructor(
    private readonly selectedYearSemService: SelectedYearSemService,
  ) {}

  // ✅ Create or update current year-semester
  @Post()
  async create(@Body() createSelectedYearSemDto: CreateSelectedYearSemDto) {
    try {
      const result = await this.selectedYearSemService.create(
        createSelectedYearSemDto,
      );
      return {
        message: 'Year and semester saved successfully',
        data: result,
      };
    } catch (error) {
      throw new HttpException(
        'Failed to save selected year and semester',
        HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }

  // ✅ Get all saved records
  @Get()
  async findAll() {
    const data = await this.selectedYearSemService.findAll();
    return { count: data.length, data };
  }

  // ✅ Get specific record by ID
  @Get(':id')
  async findOne(@Param('id') id: string) {
    const record = await this.selectedYearSemService.findOne(+id);
    if (!record) {
      throw new HttpException('Record not found', HttpStatus.NOT_FOUND);
    }
    return record;
  }

  // ✅ Update a record
  @Patch(':id')
  async update(
    @Param('id') id: string,
    @Body() updateSelectedYearSemDto: UpdateSelectedYearSemDto,
  ) {
    const updated = await this.selectedYearSemService.update(
      +id,
      updateSelectedYearSemDto,
    );
    return { message: 'Record updated successfully', data: updated };
  }

  // ✅ Delete a record
  @Delete(':id')
  async remove(@Param('id') id: string) {
    await this.selectedYearSemService.remove(+id);
    return { message: 'Record deleted successfully' };
  }
}
