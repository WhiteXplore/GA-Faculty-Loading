import { PartialType } from '@nestjs/swagger';
import { CreateActiveSemDto } from './create-active_sem.dto';

export class UpdateActiveSemDto extends PartialType(CreateActiveSemDto) {}
