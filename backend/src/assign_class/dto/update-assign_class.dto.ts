import { PartialType } from '@nestjs/swagger';
import { CreateAssignClassDto } from './create-assign_class.dto';

export class UpdateAssignClassDto extends PartialType(CreateAssignClassDto) {}
