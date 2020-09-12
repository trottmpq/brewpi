import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Container, Typography } from '@material-ui/core';
import Fab from '@material-ui/core/Fab';
import AddIcon from '@material-ui/icons/Add';
import { withStyles } from '@material-ui/styles';
import Page from 'src/components/Page';
import HeaterList from './heaterlist';

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

class Heater extends Component {
  render() {
    const { classes } = this.props;
    return (
      <Page className={classes.root} title="Heaters">
        <Container maxWidth={false}>
          <Typography variant="h1" component="h2">
            Heater List
          </Typography>
          <HeaterList/>
          <Fab
            color="primary"
            aria-label="add"
            className={classes.fab}
            onClick={() => { alert('clicked') }}
          >
            <AddIcon />
          </Fab>
        </Container>
      </Page>
    );
  }
}
Heater.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(Heater);
