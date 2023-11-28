import { Box } from '@mui/material';
import { useParams } from 'react-router-dom';

const Profile = () => {
  const { userId } = useParams();

  return <Box>Profile for user {userId}</Box>;
};

export default Profile;
