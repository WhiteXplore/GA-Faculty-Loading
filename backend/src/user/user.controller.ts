import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
  UseInterceptors,
  UploadedFile,
  BadRequestException,
} from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { UserService } from './user.service';
import { CreateUserDto, ImportUserDto } from './dto/create-user.dto';
import { UpdateUserDto } from './dto/update-user.dto';
import { ImportExpertiseDto } from './dto/import-expertise.dto';
import * as XLSX from 'xlsx';

@Controller('users')
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Post()
  async create(@Body() createUserDto: CreateUserDto) {
    return this.userService.create(createUserDto);
  }

  @Get('get-users')
  async findAll() {
    return this.userService.findAll();
  }

  // ⚠️ IMPORTANT: Import route must come BEFORE :id routes
  @Post('import-users')
  @UseInterceptors(FileInterceptor('file'))
  async importUsers(@UploadedFile() file: Express.Multer.File) {
    if (!file) {
      throw new BadRequestException('No file uploaded');
    }

    try {
      // Parse the XLSX file
      const workbook = XLSX.read(file.buffer, { type: 'buffer' });
      const sheetName = workbook.SheetNames[0];
      const worksheet = workbook.Sheets[sheetName];

      // Convert to JSON
      const rawData: any[] = XLSX.utils.sheet_to_json(worksheet, {
        raw: false,
        defval: '',
      });

      if (rawData.length === 0) {
        throw new BadRequestException('File is empty or has no valid data');
      }

      // Map columns from XLSX to ImportUserDto
      // Expected columns: "Last Name", "First Name", "Email", "Designation", "Program"
      const importData: ImportUserDto[] = rawData.map((row) => ({
        first_name: row['First Name'] || row['first_name'] || '',
        last_name: row['Last Name'] || row['last_name'] || '',
        email: row['Email'] || row['email'] || '',
        role: row['Designation'] || row['designation'] || row['role'] || '',
        program_name: row['Program'] || row['program'] || '',
      }));

      // Import users
      const results = await this.userService.importUsers(importData);

      return {
        message: 'Import completed',
        ...results,
      };
    } catch (error) {
      throw new BadRequestException(
        `Failed to process file: ${error.message}`,
      );
    }
  }

  @Get(':id')
  async findOne(@Param('id') id: string) {
    return this.userService.findOne(+id);
  }

  @Patch(':id')
  async update(@Param('id') id: string, @Body() updateUserDto: UpdateUserDto) {
    return this.userService.update(+id, updateUserDto);
  }

  @Delete(':id')
  async remove(@Param('id') id: string) {
    return this.userService.remove(+id);
  }

  @Post('import-expertise')
  @UseInterceptors(FileInterceptor('file'))
  async importExpertise(@UploadedFile() file: Express.Multer.File) {
    if (!file) {
      throw new BadRequestException('No file uploaded');
    }

    try {
      // Parse the XLSX file
      const workbook = XLSX.read(file.buffer, { type: 'buffer' });
      const sheetName = workbook.SheetNames[0];
      const worksheet = workbook.Sheets[sheetName];

      // Convert to JSON
      const rawData: any[] = XLSX.utils.sheet_to_json(worksheet, {
        raw: false,
        defval: '',
      });

      if (rawData.length === 0) {
        throw new BadRequestException('File is empty or has no valid data');
      }

      // Map columns from XLSX to ImportExpertiseDto
      // Expected columns: "Instructors Name", "Course Code"
      const importData: ImportExpertiseDto[] = rawData.map((row) => ({
        instructor_name:
          row['Instructors Name'] ||
          row['Instructor Name'] ||
          row['instructor_name'] ||
          row['Instructor'] ||
          '',
        course_code:
          row['Course Code'] || row['course_code'] || row['Code'] || '',
      }));

      // Import expertise
      const results = await this.userService.importExpertise(importData);

      return {
        message: 'Import completed',
        ...results,
      };
    } catch (error) {
      throw new BadRequestException(
        `Failed to process file: ${error.message}`,
      );
    }
  }
}
