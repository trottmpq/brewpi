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
    // myChartRef = undefined;
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
            this.props.data.push(data.temperature)
            this.props.labels.push(String(new Date().getSeconds()))
            // console.log(this.props.data)
            this.buildChart()
          })
          .catch(console.log);
      }
    buildChart = () => {
        const myChartRef = this.chartRef.current.getContext("2d");
        const { data, labels } = this.props;

        if (typeof myLineChart !== "undefined") myLineChart.destroy();

        myLineChart = new Chart(myChartRef, {
            type: "line",
            data: {
                //Bring in data
                labels: labels,
                datasets: [
                    {
                        label: "Kettle 1 Temperature",
                        data: data,
                        fill: false,
                        borderColor: "#6610f2"
                    }
                    
                ]
            },
            options: {
                //Customize chart options
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