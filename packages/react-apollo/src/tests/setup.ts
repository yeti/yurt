import { cleanup } from '@testing-library/react';
import matchers from '@testing-library/jest-dom/matchers';
import '@testing-library/jest-dom/vitest';

afterEach(() => {
  cleanup();
});

expect.extend(matchers);
