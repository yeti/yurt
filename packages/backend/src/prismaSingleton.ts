import { PrismaClient } from '~/generated/prisma/client.js';
import { mockDeep, mockReset, DeepMockProxy } from 'vitest-mock-extended';
import prisma from './prismaClient';
import { vi, beforeEach } from 'vitest';

vi.mock('./prismaClient', () => ({
  default: mockDeep<PrismaClient>(),
}));

beforeEach(() => {
  mockReset(prismaMock);
});

export const prismaMock = prisma as unknown as DeepMockProxy<PrismaClient>;
