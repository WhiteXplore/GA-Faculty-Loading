import { Injectable, InternalServerErrorException } from '@nestjs/common';
import { CreateGeneratedScheduledDto } from './dto/create-generated_scheduled.dto';
import { UpdateGeneratedScheduledDto } from './dto/update-generated_scheduled.dto';
import * as path from 'path';
import * as fs from 'fs';
import { spawn } from 'child_process';

@Injectable()
export class GeneratedScheduledService {
  create(createGeneratedScheduledDto: CreateGeneratedScheduledDto) {
    return 'This action adds a new generatedScheduled';
  }

  findAll() {
    return `This action returns all generatedScheduled`;
  }

  findOne(id: number) {
    return `This action returns a #${id} generatedScheduled`;
  }

  /**
   * ⭐ Run Python GA Scheduler
   */
  runPythonScheduler(): Promise<any> {
    return new Promise((resolve, reject) => {
      const scriptPath = path
        .resolve(__dirname, '../../../python/faculty_ga_remar.py')
        .replace(/\\/g, '/');

      console.log('Running Python script:', scriptPath);

      const pythonProcess = spawn('python', [scriptPath]);

      let stdoutData = '';
      let stderrData = '';

      pythonProcess.stdout.on('data', (data) => {
        stdoutData += data.toString();
      });

      pythonProcess.stderr.on('data', (data) => {
        stderrData += data.toString();
      });

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
          resolve(schedule);
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

  /**
   * ⭐ Read faculty loading JSON file
   */
  getFacultyLoadingFromFile() {
    try {
      const filePath = path.resolve(
        process.cwd(),
        'src',
        'generated_scheduled',
        'json_output',
        'faculty_loading.json',
      );

      if (!fs.existsSync(filePath)) {
        throw new InternalServerErrorException(
          'faculty_loading.json not found',
        );
      }

      const file = fs.readFileSync(filePath, 'utf8');

      return JSON.parse(file);
    } catch (error) {
      throw new InternalServerErrorException(
        'Failed to read faculty_loading.json',
      );
    }
  }

  update(id: number, updateGeneratedScheduledDto: UpdateGeneratedScheduledDto) {
    return `This action updates a #${id} generatedScheduled`;
  }

  remove(id: number) {
    return `This action removes a #${id} generatedScheduled`;
  }
}
