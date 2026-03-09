import {
  Controller,
  Post,
  Get,
  Body,
  Res,
  Req,
  UseGuards,
  BadRequestException,
} from '@nestjs/common';
import { AuthService } from './auth.service';
import { Response, Request } from 'express';
import { JwtAuthGuard } from './jwt-auth.guard';
import { AuthRequest } from './types';
import { UpdateUserDto } from './dto/update-user.dto';
import { Param, Patch, Delete } from '@nestjs/common';
@Controller('auth')
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  @Post('login')
  async login(
    @Body('email') email: string,
    @Body('password') password: string,
    @Res() res: Response,
  ) {
    return this.authService.login(email, password, res);
  }

  // src/auth/auth.controller.ts

  @Post('register')
  async register(
    @Body('email') email: string,
    @Body('password') password: string,
    @Body('first_name') first_name: string,
    @Body('last_name') last_name: string,
    @Body('position') position: string,

    @Body('role') role: string,
    @Body('institute_id') institute_id: number,
    @Body('program_id') program_id: number,
    @Res() res: Response,
  ) {
    if (
      !email ||
      !password ||
      !first_name ||
      !last_name ||
      !position ||
      !role ||
      !institute_id ||
      !program_id
    ) {
      throw new BadRequestException('All fields are required');
    }

    return this.authService.register(
      email,
      password,
      first_name,
      last_name,
      position,
      role,
      institute_id,
      program_id,
      res,
    );
  }

  @Post('logout')
  async logout(@Res() res: Response) {
    return this.authService.logout(res);
  }

  @Get('me')
  @UseGuards(JwtAuthGuard)
  async getProfile(@Req() req: AuthRequest) {
    return req.user; // ✅ will include institute_id and program_id now
  }

  @Get('all')
  // @UseGuards(JwtAuthGuard) // Optional: secure this route
  async getAllUsers() {
    return this.authService.getAllUsers();
  }

  @Get('all-raw')
  async getAllUsersRaw() {
    return this.authService.getAllUsersRaw();
  }

  @Patch('update/:id')
  async updateUser(@Param('id') id: number, @Body() updates: UpdateUserDto) {
    return this.authService.updateUser(Number(id), updates);
  }
  @Delete('remove/:id')
  async removeUser(@Param('id') id: number) {
    return this.authService.removeUser(+id);
  }
}
