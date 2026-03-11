import {
  Injectable,
  NotFoundException,
  BadRequestException,
} from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { User_Accounts } from './entities/user.entity';
import { CreateUserDto, ImportUserDto } from './dto/create-user.dto';
import { UpdateUserDto } from './dto/update-user.dto';
import { ImportExpertiseDto } from './dto/import-expertise.dto';
import { Program } from 'src/programs/entities/program.entity';
import { Course } from 'src/courses/entities/course.entity';
import { UserExpertise } from './entities/user_expertise.entity';
import * as bcrypt from 'bcrypt';

export interface ImportError {
  row: number;
  error: string;
  email?: string;
  data?: any;
}

export interface ImportResult {
  success: number;
  failed: number;
  errors: ImportError[];
}

@Injectable()
export class UserService {
  constructor(
    @InjectRepository(User_Accounts)
    private readonly userRepository: Repository<User_Accounts>,
    @InjectRepository(Program)
    private readonly programRepository: Repository<Program>,
    @InjectRepository(Course)
    private readonly courseRepository: Repository<Course>,
    @InjectRepository(UserExpertise)
    private readonly userExpertiseRepository: Repository<UserExpertise>,
  ) {}

  async create(createUserDto: CreateUserDto): Promise<User_Accounts> {
    const user = this.userRepository.create(createUserDto);
    return await this.userRepository.save(user);
  }

  async findAll(): Promise<User_Accounts[]> {
    return await this.userRepository.find({
      relations: [
        'institute',
        'program',
        'expertise',
        'expertise.course', // ✅ include course details
        'other_expertise',
        'other_expertise.course',
      ], // eager load relations if needed
    });
  }

  async findOne(id: number): Promise<User_Accounts> {
    const user = await this.userRepository.findOne({
      where: { id },
      relations: ['institute', 'program'],
    });
    if (!user) {
      throw new NotFoundException(`User with ID ${id} not found`);
    }
    return user;
  }

  async update(
    id: number,
    updateUserDto: UpdateUserDto,
  ): Promise<User_Accounts> {
    const user = await this.userRepository.preload({
      id,
      ...updateUserDto,
    });
    if (!user) {
      throw new NotFoundException(`User with ID ${id} not found`);
    }
    return await this.userRepository.save(user);
  }

  async remove(id: number): Promise<void> {
    const result = await this.userRepository.delete(id);
    if (result.affected === 0) {
      throw new NotFoundException(`User with ID ${id} not found`);
    }
  }

  async importUsers(importData: ImportUserDto[]): Promise<ImportResult> {
    const results: ImportResult = { success: 0, failed: 0, errors: [] };

    // Fetch all programs for matching
    const programs = await this.programRepository.find({
      relations: ['institute'],
    });

    for (let i = 0; i < importData.length; i++) {
      try {
        const userData = importData[i];

        // Validate required fields
        if (
          !userData.first_name ||
          !userData.last_name ||
          !userData.email ||
          !userData.role
        ) {
          results.failed++;
          results.errors.push({
            row: i + 2, // +2 because row 1 is header
            error: 'Missing required fields',
            data: userData,
          });
          continue;
        }

        // Check if user already exists
        const existingUser = await this.userRepository.findOne({
          where: { email: userData.email },
        });

        if (existingUser) {
          results.failed++;
          results.errors.push({
            row: i + 2,
            error: 'Email already exists',
            email: userData.email,
          });
          continue;
        }

        // Find program by name or code
        let program: Program | undefined = undefined;
        if (userData.program_name) {
          program = programs.find(
            (p) =>
              p.program_name?.toLowerCase() ===
                userData.program_name?.toLowerCase() ||
              p.program_code?.toLowerCase() ===
                userData.program_name?.toLowerCase(),
          );
        }

        // Generate a default password (can be customized)
        const defaultPassword = 'Password123!';
        const hashedPassword = await bcrypt.hash(defaultPassword, 10);

        // Create user - build object conditionally
        const userPayload: any = {
          first_name: userData.first_name.trim(),
          last_name: userData.last_name.trim(),
          email: userData.email.trim().toLowerCase(),
          password: hashedPassword,
          role: userData.role.trim(),
        };

        // Only add program and institute if program exists
        if (program) {
          userPayload.program = program;
          if (program.institute) {
            userPayload.institute = program.institute;
          }
        }

        const newUser = this.userRepository.create(userPayload);

        await this.userRepository.save(newUser);
        results.success++;
      } catch (error) {
        results.failed++;
        results.errors.push({
          row: i + 2,
          error: error.message || 'Unknown error',
          data: importData[i],
        });
      }
    }

    return results;
  }

  async importExpertise(
    importData: ImportExpertiseDto[],
  ): Promise<ImportResult> {
    const results: ImportResult = { success: 0, failed: 0, errors: [] };

    const users = await this.userRepository.find();
    const courses = await this.courseRepository.find();
    const existingExpertise = await this.userExpertiseRepository.find({
      relations: ['user', 'course'],
    });

    // -----------------------------
    // FAST LOOKUP MAPS
    // -----------------------------

    const userMap = new Map<string, User_Accounts>();
    const courseMap = new Map<string, Course>();
    const existingMap = new Set<string>();

    users.forEach((u) => {
      const key = `${u.first_name.toLowerCase()} ${u.last_name.toLowerCase()}`;
      userMap.set(key, u);
    });

    courses.forEach((c) => {
      const key = c.course_code.replace(/\s+/g, '').toUpperCase();
      courseMap.set(key, c);
    });

    existingExpertise.forEach((e) => {
      const key = `${e.user.id}-${e.course.course_id}`;
      existingMap.add(key);
    });

    const expertiseToInsert: UserExpertise[] = [];

    // -----------------------------
    // PROCESS EXCEL DATA
    // -----------------------------

    for (let i = 0; i < importData.length; i++) {
      const row = importData[i];

      if (!row.instructor_name || !row.course_code) {
        results.failed++;
        results.errors.push({
          row: i + 2,
          error: 'Missing instructor or course',
        });
        continue;
      }

      const instructor = row.instructor_name
        .trim()
        .replace(/\s+/g, ' ')
        .toLowerCase();

      const parts = instructor.split(' ');
      const first = parts[0];
      const last = parts[parts.length - 1];

      const userKey = `${first} ${last}`;
      const user = userMap.get(userKey);

      if (!user) {
        results.failed++;
        results.errors.push({
          row: i + 2,
          error: `Instructor not found: ${row.instructor_name}`,
        });
        continue;
      }

      const courseCode = row.course_code
        .trim()
        .replace(/\s+/g, '')
        .toUpperCase();

      const course = courseMap.get(courseCode);

      if (!course) {
        results.failed++;
        results.errors.push({
          row: i + 2,
          error: `Course not found: ${courseCode}`,
        });
        continue;
      }

      const key = `${user.id}-${course.course_id}`;

      if (existingMap.has(key)) {
        results.failed++;
        results.errors.push({
          row: i + 2,
          error: `Duplicate expertise`,
        });
        continue;
      }

      const expertise = this.userExpertiseRepository.create({
        user,
        course,
      });

      expertiseToInsert.push(expertise);
      existingMap.add(key);
      results.success++;
    }

    // -----------------------------
    // BULK INSERT (FAST)
    // -----------------------------

    if (expertiseToInsert.length > 0) {
      await this.userExpertiseRepository.save(expertiseToInsert);
    }

    return results;
  }
}
