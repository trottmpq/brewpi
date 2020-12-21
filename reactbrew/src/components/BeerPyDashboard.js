import React, { Component } from 'react';
import MyLineGraph from 'src/components/myLineGraph';
import Paper from '@material-ui/core/Paper';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';


export default class BeerPyDashboard extends Component {
    useStyles = makeStyles((theme) => ({
      root: {
        display: 'flex',
        flexWrap: 'wrap',
        '& > *': {
          margin: theme.spacing(1),
          width: theme.spacing(16),
          height: theme.spacing(16),
        },
      },
    }));

    state = { kettle_ids : 1}
    render() {

        return (
            <div className={this.useStyles.root}>
                <Grid container spacing={3}>
                    <Grid item xs={6}> 
                        <Paper elevation={3} >
                            <MyLineGraph  kettle_id={this.state.kettle_ids}/>
                        </Paper>
                    </Grid>
                </Grid>
            </div>
        )
    }
}

