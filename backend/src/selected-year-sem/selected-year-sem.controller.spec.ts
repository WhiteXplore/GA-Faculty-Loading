import { Test, TestingModule } from '@nestjs/testing';
import { SelectedYearSemController } from './selected-year-sem.controller';
import { SelectedYearSemService } from './selected-year-sem.service';

describe('SelectedYearSemController', () => {
  let controller: SelectedYearSemController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [SelectedYearSemController],
      providers: [SelectedYearSemService],
    }).compile();

    controller = module.get<SelectedYearSemController>(SelectedYearSemController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
