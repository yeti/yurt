import { Box, Typography } from '@mui/material';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <Box>
      <Typography>Home</Typography>
      <Link to="/user/1">User 1</Link>
    </Box>
  );
};

export default Home;
