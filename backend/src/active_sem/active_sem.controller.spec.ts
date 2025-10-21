import { Test, TestingModule } from '@nestjs/testing';
import { ActiveSemController } from './active_sem.controller';
import { ActiveSemService } from './active_sem.service';

describe('ActiveSemController', () => {
  let controller: ActiveSemController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [ActiveSemController],
      providers: [ActiveSemService],
    }).compile();

    controller = module.get<ActiveSemController>(ActiveSemController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
