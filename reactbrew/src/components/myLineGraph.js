import React, { Component } from 'react'
import Chart from "chart.js";
import classes from "./LineGraph.module.css";
let myLineChart;

//--Chart Style Options--//
// Chart.defaults.global.defaultFontFamily = "'PT Sans', sans-serif"
// Chart.defaults.global.legend.display = false;
//--Chart Style Options--//

export default class LineGraph extends Component {
    chartRef = React.createRef();
    
    state = { time : [], data1 : [], data2 : [], data3 : []};
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
        fetch("/api/devices/Kettle/1/temperature")
          .then(res => res.json())
          .then(data => {
            this.state.data1.push(data.temperature)
            this.state.time.push(new Date())
            this.buildChart()
          })
          .catch(console.log);

          fetch("/api/devices/Kettle/2/temperature")
          .then(res => res.json())
          .then(data => {
            this.state.data2.push(data.temperature)
            this.buildChart()
          })
          .catch(console.log);

          fetch("/api/devices/Kettle/3/temperature")
          .then(res => res.json())
          .then(data => {
            this.state.data3.push(data.temperature)
            this.buildChart()
          })
          .catch(console.log);


      }
    buildChart = () => {
        const myChartRef = this.chartRef.current.getContext("2d");
        // const { data, labels } = this.props;

        if (typeof myLineChart !== "undefined") myLineChart.destroy();

        myLineChart = new Chart(myChartRef, {
            type: "line",
            data: {
                //Bring in data
                labels: this.state.time,
                datasets: [
                    {
                        label: "Kettle 1 Temperature",
                        data: this.state.data1,
                        fill: false,
                        borderColor: "#6610f2"
                    },
                    {
                        label: "Kettle 2 Temperature",
                        data: this.state.data2,
                        fill: false,
                        borderColor: "#0010f2"
                    },
                    {
                        label: "Kettle 3 Temperature",
                        data: this.state.data3,
                        fill: false,
                        borderColor: "#661000"
                    }
                    
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