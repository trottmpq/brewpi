import React from 'react';
import { Component } from 'react';
import PropTypes from 'prop-types';
import { Container, Typography } from '@material-ui/core';
import { withStyles } from '@material-ui/styles';
import Page from 'src/components/Page';
import KettleCardList from './KettleCardList';
import KettleForm from './kettleform';

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

class Kettle extends Component {
  render() {
    const { classes } = this.props;
    return (
      <Page className={classes.root} title="Kettles">
        <Container maxWidth={false}>
          <Typography variant="h1" component="h2">
            Kettle List
          </Typography>
          <KettleCardList URL='/api/devices/Kettle/'/>
          <KettleForm/>
        </Container>
      </Page>
    );
  }
}

Kettle.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(Kettle);
