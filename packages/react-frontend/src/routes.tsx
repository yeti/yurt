import { Box, Typography } from '@mui/material';
import { Outlet } from 'react-router-dom';
import type { RouteObject } from 'react-router-dom';
import ErrorPage from '~/shared/components/ErrorPage';
import LoginPage from '~/modules/auth/LoginPage';
import Profile from '~/modules/profile/Profile';
import Home from '~/modules/home/Home';

const routes: RouteObject[] = [
  {
    path: '/',
    element: <LoginPage />,
    errorElement: <ErrorPage />,
  },
  {
    element: (
      <Box sx={{ backgroundColor: 'darkgray' }}>
        <Typography>Layout</Typography>
        <Outlet />
      </Box>
    ),
    children: [
      {
        path: '/home',
        element: <Home />,
      },
      {
        path: '/user/:userId',
        element: <Profile />,
      },
    ],
  },
  {
    path: '*',
    element: <Box>404</Box>,
  },
];

export { routes };
