import { Test, TestingModule } from '@nestjs/testing';
import { ActiveYearService } from './active_year.service';

describe('ActiveYearService', () => {
  let service: ActiveYearService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [ActiveYearService],
    }).compile();

    service = module.get<ActiveYearService>(ActiveYearService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
