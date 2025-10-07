import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
} from '@nestjs/common';
import { AssignClassService } from './assign_class.service';
import { CreateAssignClassDto } from './dto/create-assign_class.dto';
import { UpdateAssignClassDto } from './dto/update-assign_class.dto';

@Controller('assign-class')
export class AssignClassController {
  constructor(private readonly assignClassService: AssignClassService) {}

  @Post('add-assign-class')
  create(@Body() createAssignClassDto: CreateAssignClassDto) {
    return this.assignClassService.create(createAssignClassDto);
  }

  @Get('get-assign-class')
  findAll() {
    return this.assignClassService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.assignClassService.findOne(+id);
  }

  @Patch(':id')
  update(
    @Param('id') id: string,
    @Body() updateAssignClassDto: UpdateAssignClassDto,
  ) {
    return this.assignClassService.update(+id, updateAssignClassDto);
  }

  @Delete('delete-id/:id')
  remove(@Param('id') id: string) {
    return this.assignClassService.remove(+id);
  }
}
