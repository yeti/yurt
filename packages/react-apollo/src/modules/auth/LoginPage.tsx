import { Button, Stack, Typography } from '@mui/material';
import { useState } from 'react';
import { Link } from 'react-router-dom';

const LoginPage = () => {
  const [count, setCount] = useState(0);

  return (
    <Stack direction="column" component="main" height="100vh">
      <Stack direction="row" alignContent="center">
        <Stack direction="column" justifyContent="center" gap="10px">
          <Typography variant="h3" fontSize="30px">
            Login Page
          </Typography>
          <Typography variant="h3" fontSize="30px">
            {count}
          </Typography>
          <Button variant="contained" onClick={() => setCount(count + 1)}>
            Click
          </Button>
          <Link to="/home">
            <Button variant="contained">Login</Button>
          </Link>
        </Stack>
      </Stack>
    </Stack>
  );
};

export default LoginPage;
