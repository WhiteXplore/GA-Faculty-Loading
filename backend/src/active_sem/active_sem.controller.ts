import { Controller, Get, Post, Body, Delete, Param } from '@nestjs/common';
import { ActiveSemService } from './active_sem.service';
import { CreateActiveSemDto } from './dto/create-active_sem.dto';

@Controller('active-semester')
export class ActiveSemController {
  constructor(private readonly activeSemService: ActiveSemService) {}

  // ✅ Set active semester
  @Post()
  async setActiveSemester(@Body() createActiveSemDto: CreateActiveSemDto) {
    return await this.activeSemService.create(createActiveSemDto);
  }

  // ✅ Get current active semester
  @Get('active')
  async getActiveSemester() {
    return await this.activeSemService.findActive();
  }

  // Optional: For admin view
  @Get()
  async findAll() {
    return await this.activeSemService.findAll();
  }

  @Delete(':id')
  async remove(@Param('id') id: string) {
    return await this.activeSemService.remove(+id);
  }
}
