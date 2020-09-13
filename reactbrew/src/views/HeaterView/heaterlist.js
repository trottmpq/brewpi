import React, { Component } from 'react';
// import { makeStyles } from '@material-ui/core/styles';
// import Typography from '@material-ui/core/Typography';
import { Grid } from '@material-ui/core';
import Heater from './heater';

class HeaterList extends Component {
  state = {
    heaters: []
  };

  componentDidMount() {
    this.heaterListId = setInterval(() => this.getapi(), 1000);
  }

  componentWillUnmount() {
    clearInterval(this.heaterListId);
  }

  getapi() {
    fetch('/api/heater')
      .then(res => res.json())
      .then(data => {
        this.setState({ heaters: data });
      })
      .catch(console.log);
  }

  render() {
    return (
      <Grid container spacing={3}>
        {this.state.heaters.map(heater => (
          <Grid item lg={3} sm={6} xl={3} xs={12} key={heater.id}>
            <Heater heater={heater} />
          </Grid>
        ))}
      </Grid>
    );
  }
}

export default HeaterList;
