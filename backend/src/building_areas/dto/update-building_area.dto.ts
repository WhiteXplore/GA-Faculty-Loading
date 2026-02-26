import { PartialType } from '@nestjs/swagger';
import { CreateBuildingAreaDto } from './create-building_area.dto';

export class UpdateBuildingAreaDto extends PartialType(CreateBuildingAreaDto) {}
