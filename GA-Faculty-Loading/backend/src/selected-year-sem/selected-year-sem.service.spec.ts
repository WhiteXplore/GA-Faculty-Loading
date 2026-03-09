import { Test, TestingModule } from '@nestjs/testing';
import { SelectedYearSemService } from './selected-year-sem.service';

describe('SelectedYearSemService', () => {
  let service: SelectedYearSemService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [SelectedYearSemService],
    }).compile();

    service = module.get<SelectedYearSemService>(SelectedYearSemService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});
