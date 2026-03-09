import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { RoomsService } from './rooms.service';
import { RoomsController } from './rooms.controller';
import { Room } from './entities/room.entity';
import { Institute } from 'src/institute/entities/institute.entity';
import { Building } from 'src/buildings/entities/building.entity';
@Module({
  imports: [TypeOrmModule.forFeature([Room, Institute, Building])],
  controllers: [RoomsController],
  providers: [RoomsService],
})
export class RoomsModule {}
