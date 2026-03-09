import { Test, TestingModule } from '@nestjs/testing';
import { AssignClassController } from './assign_class.controller';
import { AssignClassService } from './assign_class.service';

describe('AssignClassController', () => {
  let controller: AssignClassController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [AssignClassController],
      providers: [AssignClassService],
    }).compile();

    controller = module.get<AssignClassController>(AssignClassController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
