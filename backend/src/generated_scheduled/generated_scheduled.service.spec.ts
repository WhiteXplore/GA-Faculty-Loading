import { Test, TestingModule } from '@nestjs/testing';
import { GeneratedScheduledService } from './generated_scheduled.service';

describe('GeneratedScheduledService', () => {
  let service: GeneratedScheduledService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [GeneratedScheduledService],
    }).compile();

    service = module.get<GeneratedScheduledService>(GeneratedScheduledService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
