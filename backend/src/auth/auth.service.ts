import {
  Injectable,
  UnauthorizedException,
  BadRequestException,
} from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Response, Request } from 'express';
import * as bcrypt from 'bcrypt';
import { User_Accounts } from 'src/user/entities/user.entity';
import { Institute } from 'src/institute/entities/institute.entity';
import { Program } from 'src/programs/entities/program.entity';
import { UpdateUserDto } from './dto/update-user.dto';
import { UserExpertise } from 'src/user/entities/user_expertise.entity';
import { UserOtherExpertise } from 'src/user/entities/user_other_expertise.entity';
import { SchoolYear } from 'src/school_year/entities/school_year.entity';
@Injectable()
export class AuthService {
  constructor(
    private readonly jwtService: JwtService,
    @InjectRepository(User_Accounts)
    private readonly userRepository: Repository<User_Accounts>,
  ) {}

  async findUserByEmail(email: string): Promise<User_Accounts | null> {
    return this.userRepository.findOne({ where: { email } });
  }

  async validateUser(email: string, password: string) {
    const user = await this.userRepository.findOne({
      where: { email },
      relations: ['institute', 'program'], // ✅ load relations
    });

    if (!user) {
      throw new UnauthorizedException('Invalid email or password');
    }

    const isPasswordValid = await bcrypt.compare(password, user.password);
    if (!isPasswordValid) {
      throw new UnauthorizedException('Invalid email or password');
    }

    return user;
  }

  async login(email: string, password: string, res: Response) {
    const user = await this.validateUser(email, password);
    const payload = {
      sub: user.id,
      email: user.email,
      role: user.role,
      first_name: user.first_name,
      last_name: user.last_name,
      institute_id: user.institute?.institute_id ?? null, // ✅ only the ID
      program_id: user.program?.program_id ?? null, // optional if you also want program_id
    };

    const token = this.jwtService.sign(payload, { expiresIn: '1h' });

    res.cookie('jwt', token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      maxAge: 3600000,
    });

    return res.json({
      message: 'Login successful',
      role: user.role,
      institute_id: user.institute?.institute_id ?? null, // ✅ also in response
      program_id: user.program?.program_id ?? null,
    });
  }

  async logout(res: Response) {
    res.clearCookie('jwt');
    return res.status(200).json({ message: 'Logged out successfully' });
  }

  async getProfile(req: Request) {
    try {
      const token = req.cookies['jwt'];
      if (!token) {
        throw new UnauthorizedException('Not authenticated');
      }

      const decoded = this.jwtService.verify(token);
      const user = await this.userRepository.findOne({
        where: { id: decoded.sub },
      });

      if (!user) {
        throw new UnauthorizedException('User not found');
      }

      return {
        id: user.id,
        email: user.email,
        role: user.role,
        first_name: user.first_name,
        last_name: user.last_name,
      };
    } catch (error) {
      throw new UnauthorizedException('Invalid or expired token');
    }
  }

  // ✅ New Registration Method
  async register(
    email: string,
    password: string,
    first_name: string,
    last_name: string,
    position: string,
    role: string,
    institute_id: number,
    program_id: number,
    res: Response,
  ) {
    const existingUser = await this.findUserByEmail(email);
    if (existingUser) {
      throw new BadRequestException('Email already in use');
    }

    const hashedPassword = await bcrypt.hash(password, 10);

    // Correct property is `id` for Institute and `program_id` for Program
    const institute = await this.userRepository.manager.findOne(Institute, {
      where: { institute_id: institute_id },
    });

    const program = await this.userRepository.manager.findOne(Program, {
      where: { program_id: program_id },
    });

    if (!institute)
      throw new BadRequestException(
        `Institute with ID ${institute_id} not found`,
      );
    if (!program)
      throw new BadRequestException(`Program with ID ${program_id} not found`);

    const newUser = this.userRepository.create({
      email,
      password: hashedPassword,
      first_name,
      last_name,
      // position,
      role,
      institute,
      program,
    });

    await this.userRepository.save(newUser);

    const payload = {
      sub: newUser.id,
      email: newUser.email,
      role: newUser.role,
      // position: newUser.position,
      first_name: newUser.first_name,
      last_name: newUser.last_name,
    };

    const token = this.jwtService.sign(payload, { expiresIn: '1h' });

    res.cookie('jwt', token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      maxAge: 3600000,
    });

    return res.status(201).json({
      message: 'Registration successful',
      role: newUser.role,
    });
  }

  // Inside AuthService
  async getAllUsers(): Promise<any[]> {
    const users = await this.userRepository.find({
      relations: ['institute', 'program'],
    });

    return users.map(({ password, institute, program, ...rest }) => ({
      ...rest,
      institute_id: institute ? institute.institute_id : null,
      program_id: program ? program.program_id : null,
    }));
  }

  async getAllUsersRaw(): Promise<User_Accounts[]> {
    return this.userRepository.find({
      relations: [
        'institute',
        'program',
        'expertise',
        'expertise.course', // ✅ include course details
        'other_expertise',
        'other_expertise.course', // ✅ include course details
      ],
    });
  }

  async updateUser(
    id: number,
    updates: UpdateUserDto,
  ): Promise<Partial<User_Accounts>> {
    const user = await this.userRepository.findOne({
      where: { id },
      relations: [
        'institute',
        'program',
        'school_year',
        'expertise',
        'other_expertise',
      ],
    });

    if (!user) {
      throw new BadRequestException(`User with ID ${id} not found`);
    }

    // Handle password change
    if (updates.password) {
      updates.password = await bcrypt.hash(updates.password, 10);
    }

    // Handle institute relation
    if (updates.institute_id) {
      const institute = await this.userRepository.manager.findOne(Institute, {
        where: { institute_id: updates.institute_id },
      });
      if (!institute) {
        throw new BadRequestException(
          `Institute with ID ${updates.institute_id} not found`,
        );
      }
      user.institute = institute;
    }

    // Handle program relation
    if (updates.program_id) {
      const program = await this.userRepository.manager.findOne(Program, {
        where: { program_id: updates.program_id },
      });
      if (!program) {
        throw new BadRequestException(
          `Program with ID ${updates.program_id} not found`,
        );
      }
      user.program = program;
    }

    // ✅ Handle school year relation
    if (updates.school_year_id) {
      const schoolYear = await this.userRepository.manager.findOne(SchoolYear, {
        where: { school_year_id: updates.school_year_id },
      });
      if (!schoolYear) {
        throw new BadRequestException(
          `School Year with ID ${updates.school_year_id} not found`,
        );
      }
      user.school_year = schoolYear;
    }

    // Handle expertise updates
    if (updates.expertise) {
      await this.userRepository.manager.delete(UserExpertise, {
        user: { id: user.id },
      });

      user.expertise = updates.expertise.map((courseId) =>
        this.userRepository.manager.create(UserExpertise, {
          course: { course_id: courseId },
          user,
        }),
      );
    }

    // Handle other_expertise updates
    if (updates.other_expertise) {
      await this.userRepository.manager.delete(UserOtherExpertise, {
        user: { id: user.id },
      });

      user.other_expertise = updates.other_expertise.map((courseId) =>
        this.userRepository.manager.create(UserOtherExpertise, {
          course: { course_id: courseId },
          user,
        }),
      );
    }

    // Assign the rest of the fields
    const {
      institute_id,
      program_id,
      school_year_id,
      expertise,
      other_expertise,
      ...rest
    } = updates;
    Object.assign(user, rest);

    const savedUser = await this.userRepository.save(user);
    const { password, ...userWithoutPassword } = savedUser;

    return userWithoutPassword;
  }

  async removeUser(id: number): Promise<{ message: string }> {
    const user = await this.userRepository.findOne({ where: { id } });

    if (!user) {
      throw new BadRequestException(`User with ID ${id} not found`);
    }

    await this.userRepository.remove(user);
    return { message: `User with ID ${id} has been removed` };
  }
}
