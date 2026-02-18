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
// import { exec } from 'child_process';
import { spawn } from 'child_process';

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
      const scriptPath = path
        .resolve(__dirname, '../../../python/faculty_ga_remar.py')
        .replace(/\\/g, '/');

      console.log('Running Python script:', scriptPath);

      const pythonProcess = spawn('python', [scriptPath]);

      let stdoutData = '';
      let stderrData = '';

      // 🔹 Collect stdout (streamed, no buffer limit)
      pythonProcess.stdout.on('data', (data) => {
        stdoutData += data.toString();
      });

      // 🔹 Collect stderr
      pythonProcess.stderr.on('data', (data) => {
        stderrData += data.toString();
      });

      // 🔹 When process finishes
      pythonProcess.on('close', (code) => {
        if (code !== 0) {
          console.error('Python error:', stderrData);
          return reject(
            new InternalServerErrorException(
              'Failed to generate faculty load.',
            ),
          );
        }

        const jsonStartMarker = '===JSON_START===';
        const jsonEndMarker = '===JSON_END===';

        const startIndex = stdoutData.indexOf(jsonStartMarker);
        const endIndex = stdoutData.indexOf(jsonEndMarker);

        if (startIndex === -1 || endIndex === -1) {
          console.error('No JSON markers found.');
          return reject(
            new InternalServerErrorException(
              'No JSON markers found in Python output.',
            ),
          );
        }

        const jsonString = stdoutData
          .substring(startIndex + jsonStartMarker.length, endIndex)
          .trim();

        try {
          const schedule = JSON.parse(jsonString);
          resolve({ success: true, data: schedule });
        } catch (err) {
          console.error('JSON parse error:', err.message);
          reject(
            new InternalServerErrorException(
              'Failed to parse JSON from Python output.',
            ),
          );
        }
      });
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
