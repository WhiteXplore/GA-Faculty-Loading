import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
  InternalServerErrorException,
} from '@nestjs/common';
import { GeneratedScheduledService } from './generated_scheduled.service';
import { CreateGeneratedScheduledDto } from './dto/create-generated_scheduled.dto';
import { UpdateGeneratedScheduledDto } from './dto/update-generated_scheduled.dto';
import { exec } from 'child_process';
import * as path from 'path';

@Controller('generated-scheduled')
export class GeneratedScheduledController {
  constructor(
    private readonly generatedScheduledService: GeneratedScheduledService,
  ) {}

  @Post()
  create(@Body() createGeneratedScheduledDto: CreateGeneratedScheduledDto) {
    return this.generatedScheduledService.create(createGeneratedScheduledDto);
  }

  @Get('load')
  getFacultyLoad() {
    return new Promise((resolve, reject) => {
      // Resolve path and replace backslashes with forward slashes
      const scriptPath = path
        .resolve(__dirname, '../../../python/faculty_ga.py')
        .replace(/\\/g, '/');
      console.log('Running Python script:', scriptPath);

      // Use double quotes around the path in exec
      exec(
        `python "${scriptPath}"`,
        { encoding: 'utf-8' },
        (error, stdout, stderr) => {
          if (error) {
            console.error('Python script error:', error.message);
            console.error(stderr);
            return reject(
              new InternalServerErrorException(
                'Failed to generate faculty load.',
              ),
            );
          }

          console.log('Python stdout:', stdout);

          // Extract JSON from stdout
          const jsonStart = stdout.indexOf('{');
          if (jsonStart === -1) {
            console.error('No JSON found in Python output.');
            return reject(
              new InternalServerErrorException(
                'No JSON found in Python output.',
              ),
            );
          }

          const jsonString = stdout.slice(jsonStart);
          try {
            const schedule = JSON.parse(jsonString);
            resolve({ success: true, data: schedule });
          } catch (parseError) {
            console.error('JSON parse error:', parseError.message);
            reject(
              new InternalServerErrorException(
                'Failed to parse JSON from Python output.',
              ),
            );
          }
        },
      );
    });
  }

  @Get()
  findAll() {
    return this.generatedScheduledService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.generatedScheduledService.findOne(+id);
  }

  @Patch(':id')
  update(
    @Param('id') id: string,
    @Body() updateGeneratedScheduledDto: UpdateGeneratedScheduledDto,
  ) {
    return this.generatedScheduledService.update(
      +id,
      updateGeneratedScheduledDto,
    );
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.generatedScheduledService.remove(+id);
  }
}
