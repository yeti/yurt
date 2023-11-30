import type { RouteObject } from 'react-router-dom';
import ErrorPage from '~/shared/components/ErrorPage';
import LoginPage from '~/modules/auth/LoginPage';
import Home from '~/modules/home/Home';
import Layout from '~/shared/components/Layout';
import NotFound from '~/shared/components/NotFound';

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
    ],
  },
  {
    path: '*',
    element: <NotFound />,
  },
];

export { routes };
