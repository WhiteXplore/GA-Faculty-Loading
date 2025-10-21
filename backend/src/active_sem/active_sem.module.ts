import { Module } from '@nestjs/common';
import { ActiveSemService } from './active_sem.service';
import { ActiveSemController } from './active_sem.controller';
import { TypeOrmModule } from '@nestjs/typeorm';
import { ActiveSem } from './entities/active_sem.entity';
@Module({
  imports: [TypeOrmModule.forFeature([ActiveSem])],
  controllers: [ActiveSemController],
  providers: [ActiveSemService],
})
export class ActiveSemModule {}
