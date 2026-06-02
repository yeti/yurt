import { Box, Typography } from "@mui/material";
import { Outlet } from "react-router-dom";

const Layout = () => (
  <Box>
    <Typography>Layout</Typography>
    <Outlet />
  </Box>
);

export default Layout;
