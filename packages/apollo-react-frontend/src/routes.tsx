import type { RouteObject } from 'react-router-dom';
import ErrorPage from '~/shared/components/ErrorPage';
import LoginPage from '~/modules/auth/LoginPage';
import Profile from '~/modules/profile/Profile';
import Home from '~/modules/home/Home';
import NotFound from '~/shared/components/NotFound';
import Layout from './shared/components/Layout';

const routes: RouteObject[] = [
  {
    path: '/',
    element: <LoginPage />,
    errorElement: <ErrorPage />,
  },
  {
    element: <Layout />,
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
    element: <NotFound />,
  },
];

export { routes };
