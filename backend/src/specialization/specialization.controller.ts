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
import { SpecializationService } from './specialization.service';
import { CreateSpecializationDto } from './dto/create-specialization.dto';
import { UpdateSpecializationDto } from './dto/update-specialization.dto';

@Controller('specialization')
export class SpecializationController {
  constructor(
    private readonly specializationService: SpecializationService,
  ) {}

  @Post('add-specialization')
  create(@Body() createSpecializationDto: CreateSpecializationDto) {
    return this.specializationService.create(createSpecializationDto);
  }

  @Get('get-specializations')
  findAll() {
    return this.specializationService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.specializationService.findOne(+id);
  }

  @Patch('update-specialization/:id')
  update(
    @Param('id') id: string,
    @Body() updateSpecializationDto: UpdateSpecializationDto,
  ) {
    return this.specializationService.update(+id, updateSpecializationDto);
  }

  @Delete('delete-id/:id')
  remove(@Param('id') id: string) {
    const numericId = parseInt(id, 10);
    if (isNaN(numericId)) {
      throw new BadRequestException('Invalid specialization ID');
    }
    return this.specializationService.remove(numericId);
  }
}

