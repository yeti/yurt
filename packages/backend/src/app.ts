// import * as Sentry from "@sentry/node";
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';

// Sentry.init({ dsn: SENTRY_DSN });

// Express server
// ----------------------------------------------------------------------------
const app = express();

// middleware
// The request handler must be the first middleware on the app
// app.use(Sentry.Handlers.requestHandler() as express.RequestHandler);
app.use(helmet());
app.use(
  cors({
    exposedHeaders: ['Authorization'],
  }),
);

// app.use(Sentry.Handlers.errorHandler());

app.get('/status', (_req, res) => {
  res.json({ status: 'ok' });
});

export default app;
