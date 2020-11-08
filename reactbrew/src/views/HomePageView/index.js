import React from 'react';
import { Container, Grid, makeStyles } from '@material-ui/core';
import Page from 'src/components/Page';
import BeerPyDashboard from 'src/components/BeerPyDashboard';
import Typography from '@material-ui/core/Typography';

const useStyles = makeStyles(theme => ({
  root: {
    backgroundColor: theme.palette.background.dark,
    minHeight: '100%',
    paddingBottom: theme.spacing(3),
    paddingTop: theme.spacing(3)
  }
}));

const HomePage = () => {
  const classes = useStyles();


  return (
    <Page className={classes.root} title="Home">
      <Container maxWidth={false}>
      <Typography variant="h1" component="h2">
            Frog Hop Brewery Dashboard
          </Typography>
        
            <BeerPyDashboard/>
      </Container>
    </Page>
  );
};

export default HomePage;
