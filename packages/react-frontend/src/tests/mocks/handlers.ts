import { http, HttpResponse } from 'msw';

export const handlers = [
  http.get('/user/:userId', () => {
    return HttpResponse.json({
      username: 'maverick',
      email: 'talk-to-me-goose@aol.com',
    });
  }),
];
