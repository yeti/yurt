import { Box, Button, TextField } from "@mui/material";
import { Controller, type SubmitHandler, useForm } from "react-hook-form";

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

  const onSubmit: SubmitHandler<FormData> = (formData) => {
    console.log(formData);
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
    </Box>
  );
};

export default Home;
