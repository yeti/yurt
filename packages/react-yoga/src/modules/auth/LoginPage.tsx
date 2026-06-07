import { Button, Stack, Typography } from "@mui/material";
import { useState } from "react";
import { Link } from "react-router-dom";

const LoginPage = () => {
  const [count, setCount] = useState(0);

  return (
    <Stack component="main" direction="column" height="100vh">
      <Stack alignContent="center" direction="row">
        <Stack direction="column" gap="10px" justifyContent="center">
          <Typography fontSize="30px" variant="h3">
            Login Page
          </Typography>
          <Typography fontSize="30px" variant="h3">
            {count}
          </Typography>
          <Button onClick={() => setCount(count + 1)} variant="contained">
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
