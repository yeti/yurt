// import * as Sentry from "@sentry/node";
// import { NODE_ENV } from "./constants";
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
// import { auth } from 'express-oauth2-jwt-bearer';
// import { unless } from "./utils/unless";
// import { DATABASE_URL, NODE_ENV } from './config';

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

// Authorization middleware. Access token must be in the headers in the following format:
// Authorization: "Bearer {accessToken}"
// const checkJwt = auth({
//   audience,
//   issuerBaseURL,
// });
// app.use(unless(["/status", "/forest"], checkJwt));

app.use(express.json({ limit: '50mb' }));
app.use(express.urlencoded({ extended: true, limit: '50mb' }));
// app.use(Sentry.Handlers.errorHandler());

app.get('/status', (_req, res) => {
  res.json({ status: 'ok' });
});

export default app;
