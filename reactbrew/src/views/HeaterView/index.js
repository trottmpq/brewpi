import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  Container,
  Grid
} from '@material-ui/core';
import { withStyles } from '@material-ui/styles';
import Page from 'src/components/Page';
import Heaters from './heaters';


const styles = theme => ({
  root: {
    backgroundColor: theme.palette.background.dark,
    minHeight: '100%',
    paddingBottom: theme.spacing(3),
    paddingTop: theme.spacing(3)
  },
});

class Heater extends Component {
  render() {
    const { classes } = this.props;
    return (
      <Page
        className={classes.root}
        title="Heaters"
      >
        <Container maxWidth={false}>
          <Grid
            container
            spacing={3}
          >
            <Grid
              item
              lg={3}
              sm={6}
              xl={3}
              xs={12}
            >
              <Heaters heaters={this.state.heaters} />
            </Grid>
          </Grid>
        </Container>
      </Page>
    )
  }

  state = {
    heaters: []
  };

  componentDidMount() {
      fetch('/api/heater')
          .then(res => res.json())
          .then((data) => {
              this.setState({ heaters: data })
          })
          .catch(console.log)
  }
}
Heater.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Heater);
