import React from 'react';
import { ApolloProvider } from '@apollo/client';
import { CssBaseline, GlobalStyles, ThemeProvider } from '@mui/material';
import ReactDOM from 'react-dom/client';
import App from '~/App.tsx';
import { globalStyles } from '~/shared/styles/global';
import { theme } from '~/shared/styles/theme';
import apolloClient from '~/apollo';

const enableMocking = async () => {
  if (import.meta.env.MODE !== 'test') {
    return;
  }

  const { worker } = await import('~/tests/mocks/browser');

  return worker.start();
};

enableMocking().then(() => {
  ReactDOM.createRoot(document.getElementById('root')!).render(
    <React.StrictMode>
      <ApolloProvider client={apolloClient}>
        <ThemeProvider theme={theme}>
          <GlobalStyles styles={globalStyles} />
          <CssBaseline enableColorScheme />
          <App />
        </ThemeProvider>
      </ApolloProvider>
    </React.StrictMode>,
  );
});
