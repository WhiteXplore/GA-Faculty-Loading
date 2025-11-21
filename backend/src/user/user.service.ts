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

    // Fetch all users and courses for matching
    const users = await this.userRepository.find();
    const courses = await this.courseRepository.find();

    for (let i = 0; i < importData.length; i++) {
      try {
        const expertiseData = importData[i];

        // Validate required fields
        if (!expertiseData.instructor_name || !expertiseData.course_code) {
          results.failed++;
          results.errors.push({
            row: i + 2, // +2 because row 1 is header
            error: 'Missing required fields',
            data: expertiseData,
          });
          continue;
        }

        // Parse instructor name (format: "Last Name, First Name M.")
        const instructorName = expertiseData.instructor_name.trim();

        // Find user by matching name (try different formats)
        let user: User_Accounts | undefined = undefined;

        // Try to match by full name comparison
        user = users.find((u) => {
          const fullName = `${u.last_name}, ${u.first_name}`;
          const fullNameReverse = `${u.first_name} ${u.last_name}`;
          const instructorLower = instructorName.toLowerCase();
          const fullNameLower = fullName.toLowerCase();
          const fullNameReverseLower = fullNameReverse.toLowerCase();

          return (
            instructorLower === fullNameLower ||
            instructorLower.includes(fullNameLower) ||
            fullNameLower.includes(instructorLower) ||
            instructorLower === fullNameReverseLower ||
            instructorLower.includes(fullNameReverseLower)
          );
        });

        if (!user) {
          results.failed++;
          results.errors.push({
            row: i + 2,
            error: `Instructor not found: ${instructorName}`,
            data: expertiseData,
          });
          continue;
        }

        // Find course by course code
        const courseCode = expertiseData.course_code.trim().toUpperCase();
        const course = courses.find(
          (c) => c.course_code.toUpperCase() === courseCode,
        );

        if (!course) {
          results.failed++;
          results.errors.push({
            row: i + 2,
            error: `Course not found: ${courseCode}`,
            data: expertiseData,
          });
          continue;
        }

        // Check if expertise already exists
        const existingExpertise = await this.userExpertiseRepository.findOne({
          where: {
            user: { id: user.id },
            course: { course_id: course.course_id },
          },
          relations: ['user', 'course'],
        });

        if (existingExpertise) {
          results.failed++;
          results.errors.push({
            row: i + 2,
            error: `Expertise already exists for ${instructorName} - ${courseCode}`,
            data: expertiseData,
          });
          continue;
        }

        // Create new expertise
        const newExpertise = this.userExpertiseRepository.create({
          user: user,
          course: course,
        });

        await this.userExpertiseRepository.save(newExpertise);
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
}
