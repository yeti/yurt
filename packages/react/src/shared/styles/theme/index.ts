import { createTheme, type ThemeOptions } from "@mui/material";
import { components } from "./components";
import { palette } from "./palette";
import { typography } from "./typography";

const themeOptions: ThemeOptions = {
  typography,
  palette,
};

export const theme = createTheme({
  ...themeOptions,
  components: {
    ...components,
  },
});
