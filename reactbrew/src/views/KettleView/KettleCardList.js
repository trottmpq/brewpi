import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Grid } from '@material-ui/core';
import KettleCard from './KettleCard';

export default class ItemCardList extends Component {
  state = {
    datalist: []
  };

  componentDidMount() {
    this.dataListId = setInterval(() => this.getapi(), 1000);
  }

  componentWillUnmount() {
    clearInterval(this.dataListId);
  }

  getapi() {
    fetch(this.props.URL)
      .then(res => res.json())
      .then(data => {
        this.setState({ datalist: data });
      })
      .catch(console.log);
  }

  render() {
    return (
      <Grid container spacing={3}>
        {this.state.datalist.map(data => (
          <Grid item lg={3} sm={6} xl={3} xs={12} key={data.id}>
            <KettleCard data={data} />
          </Grid>
        ))}
      </Grid>
    );
  }
}

ItemCardList.propTypes = {
    URL: PropTypes.object.isRequired
  };