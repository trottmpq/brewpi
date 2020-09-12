import React, { Component } from 'react';
import PropTypes from 'prop-types';
// import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import CardContent from '@material-ui/core/CardContent';
import Divider from '@material-ui/core/Divider';
import Typography from '@material-ui/core/Typography';

class Heater extends Component {
  render() {
    return (
      <Card>
        <CardHeader title={this.props.heater.name} />
        <Divider />
        <CardContent>
          <Typography color="textSecondary">
            GPIO No: {this.props.heater.gpio_num}
          </Typography>
          <Typography variant="body2" component="p">
            {this.props.heater.state}
          </Typography>
        </CardContent>
      </Card>
    );
  }
}

Heater.propTypes = {
  heater: PropTypes.object.isRequired
};

export default Heater;
