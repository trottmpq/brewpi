import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';

const useStyles = makeStyles({
  root: {
    minWidth: 275,
  },
  title: {
    fontSize: 14,
  },
  pos: {
    marginBottom: 12,
  },
});

export default function Heaters({ heaters }) {
    const classes = useStyles();

    return (
        <div>
            <Typography variant="h1" component="h2">
                Heater List
            </Typography>
            {heaters.map((heater) => (
                <Card className={classes.root}>
                <CardContent>
                    <Typography variant="h5" component="h2">
                    {heater.name}
                    </Typography>
                    <Typography className={classes.pos} color="textSecondary">
                    {heater.gpio_num}
                    </Typography>
                    <Typography variant="body2" component="p">
                    {heater.state}
                    </Typography>
                </CardContent>
                </Card>
            ))}
        </div>
        )
    }

// const Heaters = ({ heaters }) => {
//     return (
//     <div>
//         <center><h1>Heater List</h1></center>
//         {heaters.map((heater) => (
//             <Card className={classes.root}>
//             <CardContent>
//                 <Typography variant="h5" component="h2">
//                 {heater.name}
//                 </Typography>
//                 <Typography className={classes.pos} color="textSecondary">
//                 {heater.gpio_num}
//                 </Typography>
//                 <Typography variant="body2" component="p">
//                 {heater.state}
//                 </Typography>
//             </CardContent>
//             </Card>
//         ))}
//     </div>
//     )
// };

// export default Heaters