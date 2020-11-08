import React, { Component } from 'react';
import MyLineGraph from 'src/components/myLineGraph';


export default class BeerPyDashboard extends Component {
    state = {
        data: [],
        labels: []
    }

    

    render() {
        const { data, labels } = this.state;
        return (
            <div>
            {/* {console.log(data)} */}
                <MyLineGraph
                    data={data}
                    labels={labels} />
            </div>
        )
    }
}

