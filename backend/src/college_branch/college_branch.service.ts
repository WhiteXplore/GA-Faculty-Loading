import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { CollegeBranch } from './entities/college_branch.entity';
import { CreateCollegeBranchDto } from './dto/create-college_branch.dto';
import { UpdateCollegeBranchDto } from './dto/update-college_branch.dto';

@Injectable()
export class CollegeBranchService {
  constructor(
    @InjectRepository(CollegeBranch)
    private readonly collegeBranchRepo: Repository<CollegeBranch>,
  ) {}

  async create(createDto: CreateCollegeBranchDto) {
    const newBranch = this.collegeBranchRepo.create(createDto);
    return await this.collegeBranchRepo.save(newBranch);
  }

  async findAll() {
    return await this.collegeBranchRepo.find();
  }

  async findOne(id: number) {
    const branch = await this.collegeBranchRepo.findOne({
      where: { college_branch_id: id },
    });

    if (!branch) throw new NotFoundException(`College Branch #${id} not found`);

    return branch;
  }

  async update(id: number, updateDto: UpdateCollegeBranchDto) {
    const branch = await this.findOne(id);

    const updated = Object.assign(branch, updateDto);
    return await this.collegeBranchRepo.save(updated);
  }

  async remove(id: number) {
    const branch = await this.findOne(id);

    await this.collegeBranchRepo.remove(branch);
    return { message: `College Branch #${id} deleted successfully` };
  }
}
