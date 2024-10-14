import { useMutation } from '@apollo/client';
import { Box, Button, TextField } from '@mui/material';
import { useForm, Controller, SubmitHandler } from 'react-hook-form';
import { Link } from 'react-router-dom';
import { CREATE_USER } from '~/shared/mutations';

interface FormData {
  email: string;
  name: string;
}

const Home = () => {
  const {
    handleSubmit,
    control,
    formState: { errors },
  } = useForm({
    defaultValues: {
      email: '',
      name: '',
    },
  });

  const [createUser] = useMutation(CREATE_USER);

  const onSubmit: SubmitHandler<FormData> = async (formData) => {
    if (!formData.email) {
      return;
    }

    const { data } = await createUser({
      variables: {
        input: {
          name: formData.name,
          email: formData.email,
        },
      },
    });

    // eslint-disable-next-line no-console
    console.log(data);
  };

  return (
    <Box padding="16px">
      <Box
        component="form"
        onSubmit={handleSubmit(onSubmit)}
        display="flex"
        flexDirection="column"
        maxWidth="600px"
        gap="16px"
      >
        <Controller
          name="name"
          control={control}
          render={({ field }) => (
            <TextField
              label="Name"
              aria-invalid={errors.name ? 'true' : 'false'}
              {...field}
            />
          )}
        />
        <Controller
          name="email"
          control={control}
          rules={{ required: true }}
          render={({ field }) => (
            <TextField
              label="Email"
              aria-invalid={errors.email ? 'true' : 'false'}
              error={Boolean(errors.email)}
              required
              {...field}
            />
          )}
        />
        <Button type="submit" variant="contained">
          Submit
        </Button>
      </Box>
      <Link to="/user/1">User 1</Link>
    </Box>
  );
};

export default Home;
