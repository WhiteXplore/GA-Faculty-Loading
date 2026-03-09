import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { ActiveYearService } from './active_year.service';
import { ActiveYearController } from './active_year.controller';
import { ActiveYear } from './entities/active_year.entity';

@Module({
  imports: [TypeOrmModule.forFeature([ActiveYear])],
  controllers: [ActiveYearController],
  providers: [ActiveYearService],
  exports: [ActiveYearService],
})
export class ActiveYearModule {}
