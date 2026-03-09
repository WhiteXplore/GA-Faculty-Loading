import { Test, TestingModule } from '@nestjs/testing';
import { GeneratedScheduledController } from './generated_scheduled.controller';
import { GeneratedScheduledService } from './generated_scheduled.service';

describe('GeneratedScheduledController', () => {
  let controller: GeneratedScheduledController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [GeneratedScheduledController],
      providers: [GeneratedScheduledService],
    }).compile();

    controller = module.get<GeneratedScheduledController>(GeneratedScheduledController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
