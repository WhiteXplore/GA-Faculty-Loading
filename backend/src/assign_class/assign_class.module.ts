import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { AssignClass } from './entities/assign_class.entity';
import { AssignClassService } from './assign_class.service';
import { AssignClassController } from './assign_class.controller';

@Module({
  imports: [TypeOrmModule.forFeature([AssignClass])],
  controllers: [AssignClassController],
  providers: [AssignClassService],
})
export class AssignClassModule {}
