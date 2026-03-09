import { Test, TestingModule } from '@nestjs/testing';
import { AssignClassService } from './assign_class.service';

describe('AssignClassService', () => {
  let service: AssignClassService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [AssignClassService],
    }).compile();

    service = module.get<AssignClassService>(AssignClassService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
