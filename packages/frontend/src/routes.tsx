import { Box } from '@mui/material';
import { Outlet, type RouteObject } from 'react-router-dom';
import ErrorPage from '~/shared/components/ErrorPage';
import LoginPage from '~/modules/auth/LoginPage';
import Profile from '~/modules/profile/Profile';

const routes: RouteObject[] = [
  {
    path: '/',
    element: <LoginPage />,
    errorElement: <ErrorPage />,
  },
  {
    element: (
      <Box sx={{ backgroundColor: 'tomato' }}>
        Test
        <Outlet />
      </Box>
    ),
    children: [
      {
        path: '/home',
        element: <Box>Boop</Box>,
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
