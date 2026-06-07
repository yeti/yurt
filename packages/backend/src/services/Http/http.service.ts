import axios, { type AxiosInstance } from "axios";

// Need to export the class itself instead of the
// instance to be able to mock axios correctly
export class HttpService {
  readonly #axios: AxiosInstance;

  constructor() {
    this.#axios = axios.create();
  }

  get({
    endpoint,
    queryParameters,
    headers,
  }: {
    endpoint: string;
    queryParameters?: Record<string, string>;
    headers?: Record<string, string>;
  }) {
    return this.#axios.get(endpoint, { headers, params: queryParameters });
  }

  post({
    endpoint,
    body,
    headers,
  }: {
    endpoint: string;
    body?: Record<string, unknown>;
    headers?: Record<string, string>;
  }) {
    return this.#axios.post(endpoint, body, { headers });
  }
}
