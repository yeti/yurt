import { Box, Typography } from '@mui/material';
import { Outlet } from 'react-router-dom';

const Layout = () => {
  return (
    <Box>
      <Typography>Layout</Typography>
      <Outlet />
    </Box>
  );
};

export default Layout;
