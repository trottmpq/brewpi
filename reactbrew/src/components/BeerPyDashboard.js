import React, { Component } from 'react';
import KettleChart from 'src/components/KettleChart';
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
    componentDidMount() {
        this.getapi();
        // this.dataListId = setInterval(() => this.getapi(), 1000);
    }
    
      componentWillUnmount() {
        // clearInterval(this.dataListId);
      }
    
      getapi() {
        fetch("/api/devices/Kettle/")
          .then(res => res.json())
          .then(data => {
            var kettles = data.map(x => x.id);
            this.setState({kettle_ids : kettles});
          })
          .catch(console.log);
      }
    state = { kettle_ids : []}
    render() {
        return (
            <div className={this.useStyles.root}>
                <Grid container spacing={3}>
                {this.state.kettle_ids.map(data => (
                    <Grid item xs={12} key={data}> 
                        <Paper elevation={3} >
                            <KettleChart  kettle_id={data}/>
                        </Paper>
                    </Grid>
                    ))}
                </Grid>
            </div>
        )
    }
}

