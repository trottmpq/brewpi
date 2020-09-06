    // src/components/contacts.js

    import React from 'react'

    const Heaters = ({ heaters }) => {
      return (
        <div>
          <center><h1>Heater List</h1></center>
          {heaters.map((heater) => (
            <div class="card">
              <div class="card-body">
                <h5 class="card-title">{heater.name}</h5>
                <h6 class="card-subtitle mb-2 text-muted">{heater.gpio_num}</h6>
                <p class="card-text">{heater.state}</p>
              </div>
            </div>
          ))}
        </div>
      )
    };

    export default Heaters