import React, { Component } from 'react';
import MyLineGraph from 'src/components/myLineGraph';


export default class BeerPyDashboard extends Component {

    state = { kettle_ids : [1]}
    render() {

        return (
            <div>
                
                {this.state.kettle_ids.map(data => (
                    <MyLineGraph key={data} kettle_id={data}/>
                    
                    ))}
                    </div>
        )
    }
}

