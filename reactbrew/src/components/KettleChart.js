import React, { Component } from 'react'
import Chart from "chart.js";
import classes from "./LineGraph.module.css";
import PropTypes from 'prop-types';


//--Chart Style Options--//
// Chart.defaults.global.defaultFontFamily = "'PT Sans', sans-serif"
// Chart.defaults.global.legend.display = false;
//--Chart Style Options--//

export default class KettleChart extends Component {
    constructor(props) {
        super(props);
        this.chartRef = React.createRef();
        // var this.myLineChart = undefined;
      }
    state = { time : [], 
        kettle1 : { name : "", temperature : [ ], heater : [ ], target_temp : []}
        
    };
    componentDidMount() {
        this.getapi();
        this.dataListId = setInterval(() => this.getapi(), 1000);
    }
    
    componentDidUpdate() {
        this.buildChart();
    }
    
      componentWillUnmount() {
        clearInterval(this.dataListId);
      }
    
      getapi() {
        fetch("/api/devices/Kettle/".concat(this.props.kettle_id))
          .then(res => res.json())
          .then(data => {
            //   console.log(data)
            this.setState({name : data.name})
            var temps;
            if(data.temp_sensor){
                temps = this.state.kettle1.temperature;
                temps.push(data.temp_sensor.temperature)
            }
            var heat;
            if(data.heater){
                heat = this.state.kettle1.heater;
                heat.push(data.heater.state ? 100 : 0)
            }

            let target_temp = this.state.kettle1.target_temp;
            target_temp.push(data.target_temp)

            this.setState({kettle1 :{temperature : temps, heater : heat, target_temp: target_temp}})

            let times = this.state.time;
            times.push(new Date())
            this.setState({time : times})
          })
          .catch(console.log);

          


      }
    buildChart = () => {
        const myChartRef = this.chartRef.current.getContext("2d");
        // const chartid = "myChart" + this.props.kettle_id;
        // const myChartRef = document.getElementById(chartid).getContext("2d");
        if (typeof this.myLineChart !== "undefined") 
            this.myLineChart.destroy();

        this.myLineChart = new Chart(myChartRef, {
            type: "line",
            data: {
                //Bring in data
                labels: this.state.time,
                
                datasets: [
                    {
                        label: this.state.name + " Temperature",
                        data: this.state.kettle1.temperature,
                        fill: false,
                        borderColor: "#6610f2"
                    },
                    {
                        label: this.state.name + " Heater",
                        data: this.state.kettle1.heater,
                        fill: false,
                        borderColor: "#661000"
                    },
                    {
                        label: this.state.name + " Set temp",
                        data: this.state.kettle1.target_temp,
                        fill: false,
                        borderColor: "#0010f2"
                    },
                    
                ]
            },
            options: {
                //Customize chart options
                scales: {
                    yAxes: [{
                        type: 'linear',
                        ticks :{
                            min : 0,
                            max : 100
                        },
                    }],
                    xAxes: [{
                        type: 'time',
                        time: {
                            unit: 'second',
                            stepSize : 10
                        }
                    }]
                },
                animation: {
                    duration: 0
                }
            }
        });

    }

    render() {

        return (
            <div className={classes.graphContainer}>
                <canvas
                    id={"myChart" + this.props.kettle_id}
                    ref={this.chartRef}
                />
            </div>
        )
    }
}
KettleChart.propTypes = {
    kettle_id: PropTypes.number.isRequired
  };