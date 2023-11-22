import { Button, Stack, Typography } from '@mui/material';
import { useQuery } from '@apollo/client';
import { useState } from 'react';
import { Link } from 'react-router-dom';
import { GET_USER } from '~/shared/queries';

const LoginPage = () => {
  const [count, setCount] = useState(0);
  const { loading, error, data } = useQuery(GET_USER);

  console.log(data);

  if (loading) return <p>Loading...</p>;

  if (error) return <p>Error : {error.message}</p>;

  return (
    <Stack direction="column" component="main" height="100vh">
      <Stack direction="row" alignContent="center">
        <Stack direction="column" justifyContent="center">
          <Typography variant="h3" fontSize="30px">
            Login Page
          </Typography>
          <Typography variant="h3" fontSize="30px">
            {count}
          </Typography>
          <Button variant="contained" onClick={() => setCount(count + 1)}>
            Click
          </Button>
          <Link to="/test">Test Page</Link>
          <Typography variant="h3" fontSize="30px">
            {data.user.name}
          </Typography>
        </Stack>
      </Stack>
    </Stack>
  );
};

export default LoginPage;
