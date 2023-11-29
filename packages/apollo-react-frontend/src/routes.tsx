import { Box } from '@mui/material';
import { Outlet, type RouteObject } from 'react-router-dom';
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
