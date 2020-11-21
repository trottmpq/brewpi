import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import CardContent from '@material-ui/core/CardContent';
import Divider from '@material-ui/core/Divider';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/styles';
import CardActions from '@material-ui/core/CardActions';
import Grid from '@material-ui/core/Grid';
import IconButton from '@material-ui/core/IconButton';
import Switch from '@material-ui/core/Switch';
import EditIcon from '@material-ui/icons/Edit';
import Slider from '@material-ui/core/Slider';
import Dialog from '@material-ui/core/Dialog';
import KettleCardUpdate from './KettleCardUpdate'

const styles = theme => ({
  modal: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  },
  paper: {
    backgroundColor: theme.palette.background.paper,
    border: '0px solid #000',
    boxShadow: theme.shadows[5],
    padding: theme.spacing(2, 4, 3)
  },
  Icon: {
    height: 38,
    width: 38,
  },
  container: {
    display: 'grid',
    gridTemplateColumns: 'repeat(12, 1fr)',
    gridGap: theme.spacing(3),
  },
});



class ItemCard extends Component {

    state = { editOpen: false};
    showEdit = () => {
      this.setState({editOpen : true})
        
      };
    
      hideEdit = () => {
        this.setState({editOpen : false})
      };

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.checked });
    var baseStr = this.props.URL;
    var endpointStr = baseStr.concat(event.target.name)
    console.log(endpointStr)
  
    var values={ state: event.target.checked }
    setTimeout(() => {
        fetch(endpointStr, {
        method: 'PUT',
        body: JSON.stringify(values, null, 2),
        headers: { 'Content-Type': 'application/json' }
        })
        .then(res => res.json())
        .catch(error => console.error('Error:', error))
        .then(response => console.log('Success:', response));
    }, 400);

  };
 
  
  hystChange = (event, value, id) => {
    var baseStr = this.props.URL;
    var endpointStr = baseStr.concat(id)
    
    var values={ hyst_window: value }
    setTimeout(() => {
        fetch(endpointStr, {
        method: 'PUT',
        body: JSON.stringify(values, null, 2),
        headers: { 'Content-Type': 'application/json' }
        })
        .then(res => res.json())
        .catch(error => console.error('Error:', error))
        .then(response => console.log('Success:', response));
    }, 400);
  };

  tempChange = (event, value, id) => {
    var baseStr = this.props.URL;
    var endpointStr = baseStr.concat(id)
    endpointStr = endpointStr.concat("/targettemp")
    var values={ temperature: value }
    setTimeout(() => {
        fetch(endpointStr, {
        method: 'PUT',
        body: JSON.stringify(values, null, 2),
        headers: { 'Content-Type': 'application/json' }
        })
        .then(res => res.json())
        .catch(error => console.error('Error:', error))
        .then(response => console.log('Success:', response));
    }, 400);
  };


  valuetext(value) {
    return `${value}°C`;
  }


  render() {
    // const { classes } = this.props;

    return (
      <Card>
          <CardHeader title={this.props.data.name} />
          <Divider />
          <CardContent>
          
            <Grid container spacing={3}>
                <Grid item xs={6}>
                <Typography color="textSecondary">
                Temperature
                </Typography>
                </Grid>
                <Grid item xs={6}>
                <Typography color="textSecondary">
                {    this.props.data["temp_sensor"] != null ? this.props.data.temp_sensor.temperature : 0 }
                </Typography>
                </Grid>
                <Grid item xs={6}>
                <Typography color="textSecondary">
                  Pump
                </Typography>
                </Grid>
                <Grid item xs={6}>
                        <Switch
                        checked={    this.props.data["pump"] != null ? this.props.data.pump.state : false }
                        onChange={this.handleChange}
                        name={String(this.props.data.id).concat("/pumpstate")}
                        color="primary"
                        disabled = {this.props.data["pump"] != null ? false : true }
                        />
                </Grid>
                <Grid item xs={6}>
                <Typography color="textSecondary">
                Heater
                </Typography>
                </Grid>
                <Grid item xs={6}>
                    <Switch
                    checked={    this.props.data["heater"] != null ? this.props.data.heater.state : false }
                    onChange={this.handleChange}
                    name={String(this.props.data.id).concat("/heaterstate")}
                    color="primary"
                    disabled = {(this.props.data["heater"] == null || this.props.data.is_running) ? true : false }
                    />
                </Grid>
                <Grid item xs={6}>
                <Typography color="textSecondary">
                Control
                </Typography>
                </Grid>
                <Grid item xs={6}>
                    <Switch
                    checked={ this.props.data.is_running }
                    onChange={this.handleChange}
                    name={String(this.props.data.id).concat("/controlloop")}
                    color="primary"
                    disabled = {this.props.data["heater"] != null ? false : true }
                    />
                </Grid>
                <Grid item xs={6}>
                <Typography color="textSecondary">
                Target Temperature
                </Typography>
                </Grid>
                <Grid item xs={6}>
                <Slider
                    name="SetTemp"
                    defaultValue={0}
                    getAriaValueText={this.valuetext}
                    aria-labelledby="discrete-slider"
                    valueLabelDisplay="auto"
                    color="secondary"
                    step={1}
                    min={10}
                    max={100}
                    // value = {this.props.data.target_temp}
                    onChangeCommitted={(e, val) => this.tempChange(e, val, this.props.data.id)}
                    />
                </Grid>


                <Grid item xs={6}>
                <Typography color="textSecondary">
                  Hysteresis
                </Typography>
                </Grid>
                <Grid item xs={6}>
                <Slider
                    name="Hysteresis"
                    defaultValue={0}
                    getAriaValueText={this.valuetext}
                    aria-labelledby="discrete-slider"
                    valueLabelDisplay="auto"
                    color="secondary"
                    step={1}
                    min={1}
                    max={10}
                    // value = {this.props.data.target_temp}
                    onChangeCommitted={(e, val) => this.hystChange(e, val, this.props.data.id)}
                    />
                </Grid>


            </Grid>
        

        <Dialog onClose={this.showEdit} aria-labelledby="edit-dialog" open={this.state.editOpen}>
            <KettleCardUpdate handleClose={this.hideEdit} data={this.props.data} URL={this.props.URL}/>
        </Dialog>

          </CardContent>
        <CardActions>
        <IconButton aria-label="edit" onClick={this.showEdit}>
          <EditIcon />
        </IconButton>
      </CardActions>
      </Card>
    );
  }
}

ItemCard.propTypes = {
  data: PropTypes.object.isRequired,
  URL : PropTypes.string.isRequired
};

export default withStyles(styles)(ItemCard);
