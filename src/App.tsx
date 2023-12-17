import * as React from 'react';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Link from '@mui/material/Link';
import Month from './components/Month';


function Copyright() {
  return (
      <Typography variant="body2" color="text.secondary" align="center">
        {'Copyright © '}
        <Link color="inherit" href="https://mui.com/">
          John F. Salwitz
        </Link>{' '}
        {new Date().getFullYear()}.
      </Typography>
  );
}

export default function App() {
  return (

        <Box sx={{ my: 4, width: 1 }}>
            <Month></Month>
          <Copyright />
        </Box>

  );
}