import { useMutation } from "@apollo/client";
import { Box, Button, TextField } from "@mui/material";
import { Controller, type SubmitHandler, useForm } from "react-hook-form";
import { Link } from "react-router-dom";
import { CREATE_USER } from "~/shared/mutations";

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
      email: "",
      name: "",
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
        display="flex"
        flexDirection="column"
        gap="16px"
        maxWidth="600px"
        onSubmit={handleSubmit(onSubmit)}
      >
        <Controller
          control={control}
          name="name"
          render={({ field }) => (
            <TextField
              aria-invalid={errors.name ? "true" : "false"}
              label="Name"
              {...field}
            />
          )}
        />
        <Controller
          control={control}
          name="email"
          render={({ field }) => (
            <TextField
              aria-invalid={errors.email ? "true" : "false"}
              error={Boolean(errors.email)}
              label="Email"
              required
              {...field}
            />
          )}
          rules={{ required: true }}
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
