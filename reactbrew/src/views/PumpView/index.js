import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Container, Typography } from '@material-ui/core';
import { withStyles } from '@material-ui/styles';
import Page from 'src/components/Page';
import ItemCardList from 'src/components/ItemCardList';
import PumpForm from './pumppost';

const styles = theme => ({
  root: {
    backgroundColor: theme.palette.background.dark,
    minHeight: '100%',
    paddingBottom: theme.spacing(3),
    paddingTop: theme.spacing(3)
  },
  fab: {
    margin: 0,
    top: 'auto',
    left: 'auto',
    bottom: 20,
    right: 20,
    position: 'fixed'
  }
});

class Pump extends Component {
  render() {
    const { classes } = this.props;
    return (
      <Page className={classes.root} title="Pumps">
        <Container maxWidth={false}>
          <Typography variant="h1" component="h2">
            Pumps List
          </Typography>
          <ItemCardList URL='/api/pump'/>
          <PumpForm/>
        </Container>
      </Page>
    );
  }
}
Pump.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(Pump);
