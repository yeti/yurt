import axios from "axios";
import type { Mock } from "vitest";
import { vi } from "vitest";
import { HttpService } from "./http.service";

// Mock the whole axios module
vi.mock("axios");
const mockedAxios = axios as typeof axios & {
  get: Mock;
  post: Mock;
  create: Mock;
};
let httpService: HttpService;

describe("HttpService", () => {
  beforeEach(() => {
    mockedAxios.create.mockReturnThis();
    httpService = new HttpService();
  });

  afterEach(() => {
    // Clear all mocks after each test
    vi.clearAllMocks();
  });

  it("should make a GET request with correct parameters", async () => {
    // Setup mock to resolve with specific data
    mockedAxios.get.mockResolvedValue({ data: "response data" });

    const endpoint = "http://example.com/data";
    const params = { foo: "bar", baz: "qux" };
    const headers = { Authorization: "Bearer token" };

    // Call the method
    const response = await httpService.get({
      endpoint,
      queryParameters: params,
      headers,
    });

    // Check if axios.get was called correctly
    expect(mockedAxios.get).toHaveBeenCalledWith(endpoint, {
      headers,
      params,
    });
    // Check the response
    expect(response.data).toBe("response data");
  });

  it("should make a POST request with correct parameters", async () => {
    mockedAxios.post.mockResolvedValue({ data: "response data" });

    const endpoint = "http://example.com/submit";
    const body = { list: [1, 2, 3], isValid: true };
    const headers = { "Content-Type": "application/json" };

    const response = await httpService.post({ endpoint, body, headers });

    expect(mockedAxios.post).toHaveBeenCalledWith(endpoint, body, {
      headers,
    });
    expect(response.data).toBe("response data");
  });
});
