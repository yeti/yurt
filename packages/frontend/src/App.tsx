import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import ErrorPage from '~/shared/components/ErrorPage';
import LoginPage from '~/modules/auth/LoginPage';
import { Box } from '@mui/material';

const App = () => {
  const router = createBrowserRouter([
    {
      path: '/',
      element: <LoginPage />,
      errorElement: <ErrorPage />,
    },
    {
      path: '/test',
      element: <Box>Test</Box>,
    },
    {
      path: '*',
      element: <Box>404</Box>,
    },
  ]);

  return <RouterProvider router={router} />;
};

export default App;
