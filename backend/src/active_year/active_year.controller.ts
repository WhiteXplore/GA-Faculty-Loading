import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
} from '@nestjs/common';
import { ActiveYearService } from './active_year.service';
import { CreateActiveYearDto } from './dto/create-active_year.dto';
import { UpdateActiveYearDto } from './dto/update-active_year.dto';

@Controller('active-year')
export class ActiveYearController {
  constructor(private readonly activeYearService: ActiveYearService) {}

  // ✅ Set (or switch) the active year
  @Post()
  setActiveYear(@Body() createActiveYearDto: CreateActiveYearDto) {
    return this.activeYearService.setActiveYear(createActiveYearDto);
  }

  // ✅ Get all years
  @Get()
  findAll() {
    return this.activeYearService.findAll();
  }

  // ✅ Get current active year
  @Get('active')
  getActiveYear() {
    return this.activeYearService.getActiveYear();
  }

  // ✅ Get one by ID
  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.activeYearService.findOne(+id);
  }

  // ✅ Update by ID
  @Patch(':id')
  update(
    @Param('id') id: string,
    @Body() updateActiveYearDto: UpdateActiveYearDto,
  ) {
    return this.activeYearService.update(+id, updateActiveYearDto);
  }

  // ✅ Delete by ID
  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.activeYearService.remove(+id);
  }
}
