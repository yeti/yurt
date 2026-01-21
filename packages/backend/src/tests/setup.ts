import { beforeEach } from 'vitest';
import { mockReset } from 'vitest-mock-extended';
import { prismaMock } from '~/prismaSingleton';

beforeEach(() => {
  mockReset(prismaMock);
});
