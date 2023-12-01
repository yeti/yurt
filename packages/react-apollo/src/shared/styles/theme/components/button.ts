import { Components, Theme } from '@mui/material';

export const MuiButton: Components<Theme>['MuiButton'] = {
  variants: [
    {
      props: { variant: 'contained' },
      style: ({ theme }) => {
        return {
          color: theme.palette.common.white,
          backgroundColor: theme.palette.common.black,
          width: '100%',
          textAlign: 'center',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontWeight: 700,
          fontSize: 18,
          boxShadow: 'none',

          '&:hover': {
            boxShadow: 'none',
          },

          '&:disabled': {
            cursor: 'not-allowed',
          },
        };
      },
    },
  ],
};
