import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardHeader from '@material-ui/core/CardHeader';
import CardContent from '@material-ui/core/CardContent';
import Divider from '@material-ui/core/Divider';
import Typography from '@material-ui/core/Typography';

export default class ItemCard extends Component {
  render() {
    console.log(this.props.data);
    return (
      <Card>
        <CardActionArea
          onClick={() => {
            alert('clicked');
          }}
        >
          <CardHeader title={this.props.data.name} />
          <Divider />
          <CardContent>
            {Object.keys(this.props.data).map((key, i) => (
              <Typography color="textSecondary">
                {key}:{' '}
                {this.props.data[key] === null
                  ? 'Unkown'
                  : this.props.data[key].toString()}
              </Typography>
            ))}
          </CardContent>
        </CardActionArea>
      </Card>
    );
  }
}

ItemCard.propTypes = {
  data: PropTypes.object.isRequired
};
