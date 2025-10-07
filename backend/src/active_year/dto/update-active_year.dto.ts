import { PartialType } from '@nestjs/swagger';
import { CreateActiveYearDto } from './create-active_year.dto';

export class UpdateActiveYearDto extends PartialType(CreateActiveYearDto) {}
