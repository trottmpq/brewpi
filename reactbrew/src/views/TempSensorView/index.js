import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Container, Typography } from '@material-ui/core';
import { withStyles } from '@material-ui/styles';
import Page from 'src/components/Page';
import ItemCardList from 'src/components/ItemCardList';
import ItemCardCreate from 'src/components/ItemCardCreate';
import Dialog from '@material-ui/core/Dialog';
import Fab from '@material-ui/core/Fab';
import AddIcon from '@material-ui/icons/Add';

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

class TempSensor extends Component {
  state = { createOpen: false}
  openCreate = () => {
    console.log("Opening create dialog")
    this.setState({createOpen: true})
  }

  closeCreate = () => {
    console.log("Closing create dialog")
    this.setState({createOpen: false})
  }
  render() {
    const { classes } = this.props;
    return (
      <Page className={classes.root} title="Temperature Sensors">
        <Container maxWidth={false}>
          <Typography variant="h1" component="h2">
            Temp Sensor List
          </Typography>
          <ItemCardList URL='/api/devices/TempSensor/' type={"TempSensor"}/>
          <Dialog onClose={this.closeCreate} open={this.state.createOpen}>
            <ItemCardCreate URL='/api/devices/TempSensor/' handleClose={this.closeCreate}/>
          </Dialog>
        </Container>
        <Fab
        color="secondary"
        aria-label="add"
        className={classes.fab}
        onClick={this.openCreate}
      ><AddIcon />
      </Fab>
      </Page>
    );
  }
}

TempSensor.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(TempSensor);
