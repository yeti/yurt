import { ApolloProvider } from "@apollo/client";
import { CssBaseline, GlobalStyles, ThemeProvider } from "@mui/material";
import React from "react";
import ReactDOM from "react-dom/client";
import App from "~/App.tsx";
import apolloClient from "~/apollo";
import { globalStyles } from "~/shared/styles/global";
import { theme } from "~/shared/styles/theme";

const enableMocking = async () => {
  if (import.meta.env.MODE !== "test") {
    return;
  }

  const { worker } = await import("~/tests/mocks/browser");

  return worker.start();
};

enableMocking().then(() => {
  const rootElement = document.getElementById("root");
  if (!rootElement) {
    throw new Error("Root element #root not found");
  }

  ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
      <ApolloProvider client={apolloClient}>
        <ThemeProvider theme={theme}>
          <GlobalStyles styles={globalStyles} />
          <CssBaseline enableColorScheme />
          <App />
        </ThemeProvider>
      </ApolloProvider>
    </React.StrictMode>
  );
});
