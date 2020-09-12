import React, { Component } from 'react';
import PropTypes from 'prop-types';
// import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardHeader from '@material-ui/core/CardHeader';
import CardContent from '@material-ui/core/CardContent';
import Divider from '@material-ui/core/Divider';
import Typography from '@material-ui/core/Typography';

class Heater extends Component {
  render() {
    console.log(this.props.heater);
    return (
      <Card>
        <CardActionArea onClick={() => { alert('clicked') }}>
        <CardHeader title={this.props.heater.name} />
        <Divider />
        <CardContent>
          <Typography color="textSecondary">
            GPIO No: {this.props.heater.gpio_num}
          </Typography>
          <Typography color="textSecondary">
            Active Low: {this.props.heater.activeLow.toString()}
          </Typography>
          <Typography color="textSecondary">
            Current State: {this.props.heater.state.toString()}
          </Typography>
        </CardContent>
        </CardActionArea>
      </Card>
    );
  }
}

Heater.propTypes = {
  heater: PropTypes.object.isRequired
};

export default Heater;
