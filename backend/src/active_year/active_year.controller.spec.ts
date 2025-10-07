import { Test, TestingModule } from '@nestjs/testing';
import { ActiveYearController } from './active_year.controller';
import { ActiveYearService } from './active_year.service';

describe('ActiveYearController', () => {
  let controller: ActiveYearController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [ActiveYearController],
      providers: [ActiveYearService],
    }).compile();

    controller = module.get<ActiveYearController>(ActiveYearController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
