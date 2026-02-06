import { useQuery } from '@apollo/client';
import { Box, Typography } from '@mui/material';
import { Link, useParams } from 'react-router-dom';
import { GET_USER } from '~/shared/queries';

const Profile = () => {
  const params = useParams();

  const { loading, error, data } = useQuery(GET_USER, {
    variables: { userId: Number(params.userId) },
  });

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>Error : {error.message}</p>;
  }

  return (
    <Box>
      <Typography>
        Profile for user {params.userId}: {data.user.email}
      </Typography>
      <Link to={'/home'}>Back to home</Link>
    </Box>
  );
};

export default Profile;
