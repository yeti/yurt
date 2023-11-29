import { Box, Button, TextField, Typography } from '@mui/material';
import { useForm, Controller, SubmitHandler } from 'react-hook-form';
import { Link } from 'react-router-dom';

interface FormData {
  email: string;
  name: string;
}

const Home = () => {
  const { handleSubmit, control } = useForm({
    defaultValues: {
      email: '',
      name: '',
    },
  });

  const onSubmit: SubmitHandler<FormData> = (data) => {
    console.log(data);
  };

  return (
    <Box padding="16px">
      <Box
        component="form"
        onSubmit={handleSubmit(onSubmit)}
        display="flex"
        flexDirection="column"
      >
        <Controller
          name="name"
          control={control}
          render={({ field }) => <TextField label="Create User" {...field} />}
        />
        <Controller
          name="email"
          control={control}
          render={({ field }) => <TextField label="Email" {...field} />}
        />
        <Button type="submit">Submit</Button>
      </Box>
      <Link to="/user/1">User 1</Link>
    </Box>
  );
};

export default Home;
