import { Test, TestingModule } from '@nestjs/testing';
import { ActiveSemService } from './active_sem.service';

describe('ActiveSemService', () => {
  let service: ActiveSemService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [ActiveSemService],
    }).compile();

    service = module.get<ActiveSemService>(ActiveSemService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
