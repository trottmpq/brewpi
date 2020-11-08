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
import DeleteForeverIcon from '@material-ui/icons/DeleteForever';
import Switch from '@material-ui/core/Switch';
import EditIcon from '@material-ui/icons/Edit';
import Slider from '@material-ui/core/Slider';

import Dialog from '@material-ui/core/Dialog';
import Button from '@material-ui/core/Button';
import MuiDialogTitle from '@material-ui/core/DialogTitle';
import MuiDialogContent from '@material-ui/core/DialogContent';
import MuiDialogActions from '@material-ui/core/DialogActions';
import CloseIcon from '@material-ui/icons/Close';

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
const DialogTitle = withStyles(styles)((props) => {
    const { children, classes, onClose, ...other } = props;
    return (
      <MuiDialogTitle disableTypography className={classes.root} {...other}>
        <Typography variant="h6">{children}</Typography>
        {onClose ? (
          <IconButton aria-label="close" className={classes.closeButton} onClick={onClose}>
            <CloseIcon />
          </IconButton>
        ) : null}
      </MuiDialogTitle>
    );
  });
  
  const DialogContent = withStyles((theme) => ({
    root: {
      padding: theme.spacing(2),
    },
  }))(MuiDialogContent);
  
  const DialogActions = withStyles((theme) => ({
    root: {
      margin: 0,
      padding: theme.spacing(1),
    },
  }))(MuiDialogActions);


class ItemCard extends Component {

    state = { editOpen: false};
    showEdit = () => {
        console.log("editOpen <= true")
        this.state.editOpen = true;
      };
    
      hideEdit = () => {
        console.log("editOpen <= false")
        this.state.editOpen = false;
      };

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.checked });
    var baseStr = "/devices/Kettle/"
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

  tempChange = (event, value, id) => {
    var baseStr = "/devices/Kettle/"
    var endpointStr = baseStr.concat(id)
    var values={ target_temp: value }
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
    const { classes } = this.props;

    return (
      <Card>
          <CardHeader title={this.props.data.name} />
          <Divider />
          <CardContent>
          <Typography color="textSecondary">
            <Grid container spacing={3}>
                <Grid item xs={6}>
                Temperature
                </Grid>
                <Grid item xs={6}>
                {    this.props.data["temp_sensor"] != null ? this.props.data.temp_sensor.temperature : 0 }
                </Grid>
                <Grid item xs={6}>
                Pump
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
                Heater
                </Grid>
                <Grid item xs={6}>
                    <Switch
                    checked={    this.props.data["heater"] != null ? this.props.data.heater.state : false }
                    onChange={this.handleChange}
                    name={String(this.props.data.id).concat("/heaterstate")}
                    color="primary"
                    disabled = {this.props.data["heater"] != null ? false : true }
                    />
                </Grid>
                <Grid item xs={6}>
                Target Temperaure
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
            </Grid>
        </Typography>
        
        <Dialog onClose={this.showEdit} aria-labelledby="edit-dialog" open={this.state.editOpen}>
            <KettleCardUpdate handleClose={this.hideEdit} data={this.props.data}/>
        </Dialog>

          </CardContent>
        <CardActions>
        <IconButton aria-label="edit">
                <EditIcon className={classes.Icon} onClick={this.showEdit}/>
                </IconButton>
            <IconButton aria-label="delete">
                <DeleteForeverIcon className={classes.Icon} />
            </IconButton>
      </CardActions>
      </Card>
    );
  }
}

ItemCard.propTypes = {
  data: PropTypes.object.isRequired
};

export default withStyles(styles)(ItemCard);
