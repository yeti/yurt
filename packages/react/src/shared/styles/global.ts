import { css } from '@mui/material';
import { theme } from '~/shared/styles/theme';

export const globalStyles = css`
  body,
  html,
  #root {
    height: 100%;
    margin: 0;
    padding: 0;
    background-color: ${theme.palette.common.white};
    font-family: sans-serif;
  }
`;
