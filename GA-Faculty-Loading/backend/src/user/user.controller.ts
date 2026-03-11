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

  // CREATE USER
  @Post()
  async create(@Body() createUserDto: CreateUserDto) {
    return this.userService.create(createUserDto);
  }

  // GET ALL USERS
  @Get('get-users')
  async findAll() {
    return this.userService.findAll();
  }

  // ===============================
  // IMPORT USERS
  // ===============================
  @Post('import-users')
  @UseInterceptors(FileInterceptor('file'))
  async importUsers(@UploadedFile() file: Express.Multer.File) {
    if (!file) {
      throw new BadRequestException('No file uploaded');
    }

    if (!file.originalname.endsWith('.xlsx')) {
      throw new BadRequestException('Only .xlsx files are allowed');
    }

    try {
      const workbook = XLSX.read(file.buffer, { type: 'buffer' });
      const sheetName = workbook.SheetNames[0];
      const worksheet = workbook.Sheets[sheetName];

      const rawData: any[] = XLSX.utils.sheet_to_json(worksheet, {
        raw: false,
        defval: '',
      });

      if (!rawData.length) {
        throw new BadRequestException('Excel file is empty');
      }

      const importData: ImportUserDto[] = rawData.map((row) => ({
        first_name: row['First Name'] || row['first_name'] || '',
        last_name: row['Last Name'] || row['last_name'] || '',
        email: row['Email'] || row['email'] || '',
        role: row['Designation'] || row['designation'] || row['role'] || '',
        program_name: row['Program'] || row['program'] || '',
      }));

      const results = await this.userService.importUsers(importData);

      return {
        message: 'Users imported successfully',
        ...results,
      };
    } catch (error) {
      throw new BadRequestException(`Failed to process file: ${error.message}`);
    }
  }

  // ===============================
  // IMPORT USER EXPERTISE
  // ===============================
  @Post('import-expertise')
  @UseInterceptors(FileInterceptor('file'))
  async importExpertise(@UploadedFile() file: Express.Multer.File) {
    if (!file) {
      throw new BadRequestException('No file uploaded');
    }

    if (!file.originalname.endsWith('.xlsx')) {
      throw new BadRequestException('Only .xlsx files are allowed');
    }

    try {
      const workbook = XLSX.read(file.buffer, { type: 'buffer' });
      const sheetName = workbook.SheetNames[0];
      const worksheet = workbook.Sheets[sheetName];

      const rawData: any[] = XLSX.utils.sheet_to_json(worksheet, {
        raw: false,
        defval: '',
      });

      if (!rawData.length) {
        throw new BadRequestException('Excel file is empty');
      }

      const importData: ImportExpertiseDto[] = rawData.map((row) => ({
        instructor_name:
          row['Instructors Name'] ||
          row['Instructor Name'] ||
          row['Instructor'] ||
          row['instructor_name'] ||
          '',
        course_code:
          row['Course Code'] ||
          row['course_code'] ||
          row['Course'] ||
          row['Code'] ||
          '',
      }));

      const results = await this.userService.importExpertise(importData);

      return {
        message: 'Expertise imported successfully',
        ...results,
      };
    } catch (error) {
      throw new BadRequestException(`Failed to process file: ${error.message}`);
    }
  }

  // ===============================
  // GET USER BY ID
  // ===============================
  @Get(':id')
  async findOne(@Param('id') id: string) {
    return this.userService.findOne(+id);
  }

  // ===============================
  // UPDATE USER
  // ===============================
  @Patch(':id')
  async update(@Param('id') id: string, @Body() updateUserDto: UpdateUserDto) {
    return this.userService.update(+id, updateUserDto);
  }

  // ===============================
  // DELETE USER
  // ===============================
  @Delete(':id')
  async remove(@Param('id') id: string) {
    return this.userService.remove(+id);
  }
}
