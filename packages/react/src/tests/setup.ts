import matchers from "@testing-library/jest-dom/matchers";
import { cleanup } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";

afterEach(() => {
  cleanup();
});

expect.extend(matchers);
