import React, { Component } from 'react'
import Chart from "chart.js";
import classes from "./LineGraph.module.css";
import PropTypes from 'prop-types';
let myLineChart;

//--Chart Style Options--//
// Chart.defaults.global.defaultFontFamily = "'PT Sans', sans-serif"
// Chart.defaults.global.legend.display = false;
//--Chart Style Options--//

export default class LineGraph extends Component {
    chartRef = React.createRef();
    
    state = { time : [], 
        kettle1 : { temperature : [ ], heater : [ ], target_temp : []}
        
    };
    componentDidMount() {
        this.buildChart();
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
            let temps = this.state.kettle1.temperature;
            temps.push(data.temp_sensor.temperature)
 
            let heat = this.state.kettle1.heater;
            heat.push(data.heater.state ? 100 : 0)

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

        if (typeof myLineChart !== "undefined") myLineChart.destroy();

        myLineChart = new Chart(myChartRef, {
            type: "line",
            data: {
                //Bring in data
                labels: this.state.time,
                
                datasets: [
                    {
                        label: "Kettle 1 Temperature",
                        data: this.state.kettle1.temperature,
                        fill: false,
                        borderColor: "#6610f2"
                    },
                    {
                        label: "Kettle 1 Heater",
                        data: this.state.kettle1.heater,
                        fill: false,
                        borderColor: "#661000"
                    },
                    {
                        label: "Kettle Set temp",
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
                    id="myChart"
                    ref={this.chartRef}
                />
            </div>
        )
    }
}
LineGraph.propTypes = {
    kettle_id: PropTypes.number.isRequired
  };