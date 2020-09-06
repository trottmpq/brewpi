import React, { Component } from 'react';
import {
  Container,
  Grid,
  makeStyles
} from '@material-ui/core';
import Page from 'src/components/Page';
import Heaters from './heaters';


const useStyles = makeStyles((theme) => ({
  root: {
    backgroundColor: theme.palette.background.dark,
    minHeight: '100%',
    paddingBottom: theme.spacing(3),
    paddingTop: theme.spacing(3)
  }
}));

// const Heater = () => {
  // const classes = useStyles();

//   const [currentHeaters, setCurrentHeaters] = useState(0);

//   useEffect(() => {
//     fetch('/api/heater').then(res => res.json()).then(data => {
//       setCurrentHeaters(data);
//     });
//   }, []);

//   return (
//     <Page
//       className={classes.root}
//       title="Heaters"
//     >
//       <Container maxWidth={false}>
//         <Grid
//           container
//           spacing={3}
//         >
//           <Grid
//             item
//             lg={3}
//             sm={6}
//             xl={3}
//             xs={12}
//           >
//             <Heaters heaters={currentHeaters} />
//           </Grid>
//         </Grid>
//       </Container>
//     </Page>
//   );
// };

class Heater extends Component {
  render() {
    return (
      <Page
        // className={classes.root}
        title="Heaters"
      >
        <Container maxWidth={false}>
          <Grid
            container
            spacing={3}
          >
            <Grid
              item
              lg={3}
              sm={6}
              xl={3}
              xs={12}
            >
              <Heaters heaters={this.state.heaters} />
            </Grid>
          </Grid>
        </Container>
      </Page>
    )
  }

  state = {
    heaters: []
  };

  componentDidMount() {
      fetch('/api/heater')
          .then(res => res.json())
          .then((data) => {
              this.setState({ heaters: data })
          })
          .catch(console.log)
  }
}

export default Heater;
