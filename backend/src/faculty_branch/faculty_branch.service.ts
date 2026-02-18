import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository, In } from 'typeorm';

import { FacultyBranch } from './entities/faculty_branch.entity';
import { CreateFacultyBranchDto } from './dto/create-faculty_branch.dto';
import { UpdateFacultyBranchDto } from './dto/update-faculty_branch.dto';
import { User_Accounts } from 'src/user/entities/user.entity';
import { CollegeBranch } from 'src/college_branch/entities/college_branch.entity';

@Injectable()
export class FacultyBranchService {
  constructor(
    @InjectRepository(FacultyBranch)
    private facultyBranchRepo: Repository<FacultyBranch>,

    @InjectRepository(User_Accounts)
    private userRepo: Repository<User_Accounts>,

    @InjectRepository(CollegeBranch)
    private branchRepo: Repository<CollegeBranch>,
  ) {}

  // ✅ CREATE (single)
  async create(dto: CreateFacultyBranchDto) {
    const { user_id, college_branch_id } = dto;

    const user = await this.userRepo.findOne({ where: { id: user_id } });
    if (!user) throw new NotFoundException('User not found');

    const branch = await this.branchRepo.findOne({
      where: { college_branch_id },
    });
    if (!branch) throw new NotFoundException('College branch not found');

    const facultyBranch = this.facultyBranchRepo.create({
      user,
      collegeBranch: branch,
    });
    return this.facultyBranchRepo.save(facultyBranch);
  }

  // ✅ FIND ALL
  async findAll() {
    return this.facultyBranchRepo.find({
      relations: ['user', 'collegeBranch'],
    });
  }

  // ✅ FIND ONE
  async findOne(id: number) {
    const facultyBranch = await this.facultyBranchRepo.findOne({
      where: { faculty_branch_id: id },
      relations: ['user', 'collegeBranch'],
    });
    if (!facultyBranch) throw new NotFoundException('FacultyBranch not found');
    return facultyBranch;
  }

  // ✅ UPDATE (single)
  async update(id: number, dto: UpdateFacultyBranchDto) {
    const facultyBranch = await this.facultyBranchRepo.findOne({
      where: { faculty_branch_id: id },
      relations: ['user', 'collegeBranch'],
    });
    if (!facultyBranch) throw new NotFoundException('FacultyBranch not found');

    if (dto.user_id) {
      const user = await this.userRepo.findOne({ where: { id: dto.user_id } });
      if (!user) throw new NotFoundException('User not found');
      facultyBranch.user = user;
    }

    if (dto.college_branch_id) {
      const branch = await this.branchRepo.findOne({
        where: { college_branch_id: dto.college_branch_id },
      });
      if (!branch) throw new NotFoundException('College branch not found');
      facultyBranch.collegeBranch = branch;
    }

    return this.facultyBranchRepo.save(facultyBranch);
  }

  // ✅ REMOVE
  async remove(id: number) {
    const facultyBranch = await this.findOne(id);
    await this.facultyBranchRepo.remove(facultyBranch);
    return { message: 'Deleted successfully' };
  }

  // ✅ BATCH UPDATE: Assign multiple branches to a user
  async updateUserBranches(user_id: number, college_branch_ids: number[]) {
    const user = await this.userRepo.findOne({ where: { id: user_id } });
    if (!user) throw new NotFoundException('User not found');

    // Delete old branches
    await this.facultyBranchRepo.delete({ user: { id: user_id } });

    // Find all branches
    const branches = await this.branchRepo.find({
      where: { college_branch_id: In(college_branch_ids) },
    });
    if (branches.length !== college_branch_ids.length)
      throw new NotFoundException('One or more college branches not found');

    // Create new faculty branch records
    const newFacultyBranches = branches.map((branch) =>
      this.facultyBranchRepo.create({ user, collegeBranch: branch }),
    );

    return this.facultyBranchRepo.save(newFacultyBranches);
  }
}
