import { Box, Button } from '@mui/material';
import { Link } from 'react-router-dom';

const NotFound = () => {
  return (
    <Box sx={{ placeItems: 'center' }}>
      404
      <Link to="/">
        <Button>Go back home</Button>
      </Link>
    </Box>
  );
};

export default NotFound;
