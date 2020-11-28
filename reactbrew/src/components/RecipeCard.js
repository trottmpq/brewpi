import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import clsx from 'clsx';
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import CardContent from '@material-ui/core/CardContent';
import CardActions from '@material-ui/core/CardActions';
import Collapse from '@material-ui/core/Collapse';
import IconButton from '@material-ui/core/IconButton';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import MoreVertIcon from '@material-ui/icons/MoreVert';
import PropTypes from 'prop-types';
import { FaBeer } from 'react-icons/fa';
import StarBorderIcon from '@material-ui/icons/StarBorder';
import StarIcon from '@material-ui/icons/Star';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';


const useStyles = makeStyles((theme) => ({
  root: {
    
  },
  media: {
    height: 0,
    paddingTop: '56.25%', // 16:9
  },
  expand: {
    transform: 'rotate(0deg)',
    marginLeft: 'auto',
    transition: theme.transitions.create('transform', {
      duration: theme.transitions.duration.shortest,
    }),
  },
  expandOpen: {
    transform: 'rotate(180deg)',
  },
  table: {
    minWidth: 10,
  },
}));

function InfoTable(props) {
    const classes = useStyles();
  
    return (
      <TableContainer component={Paper}>
        <Table className={classes.table} size="small" aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>Batch Size</TableCell>
              <TableCell >OG</TableCell>
              <TableCell >FG</TableCell>
              <TableCell >ABV</TableCell>
              
            </TableRow>
          </TableHead>
          <TableBody>
              <TableRow key={props.data.name}>
                <TableCell > {props.data.batch_size.toFixed(2)} </TableCell>
                <TableCell >{props.data.og}</TableCell>
                <TableCell >{props.data.fg}</TableCell>
                <TableCell >{props.data.abv.toFixed(2)}</TableCell>
              </TableRow>
          </TableBody>
        </Table>
      </TableContainer>
    );
  }
  InfoTable.propTypes = {
    data: PropTypes.object.isRequired
  };

  function FermentableTable(props) {
    const classes = useStyles();
  
    return (
      <TableContainer component={Paper}>
        <Table className={classes.table} size="small" aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell >Amount (kg)</TableCell>
              <TableCell >Colour (&deg;L)</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
              {props.data.fermentables.map((fermentable) =>(
              <TableRow key={fermentable.name}>
                <TableCell > {fermentable.name} </TableCell>
                <TableCell >{fermentable.amount.toFixed(2)}</TableCell>
                <TableCell >{fermentable.color}</TableCell>
              </TableRow>
              ))}
          </TableBody>
        </Table>
      </TableContainer>
    );
  }
  FermentableTable.propTypes = {
    data: PropTypes.object.isRequired
  };

  function HopTable(props) {
    const classes = useStyles();
  
    return (
      <TableContainer component={Paper}>
        <Table className={classes.table} size="small" aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell >Amount (g)</TableCell>
              <TableCell >Use</TableCell>
              <TableCell >Time</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
              {props.data.hops.map((hop, index) =>(
              <TableRow key={index}>
                <TableCell > {hop.name} </TableCell>
                <TableCell >{(hop.amount*1000).toFixed(2)}</TableCell>
                <TableCell >{hop.use}</TableCell>
                <TableCell >{(hop.time < props.data.boil_time) ? (hop.time + " mins") : (hop.time/60/24 + " days")}</TableCell>
              </TableRow>
              ))}
          </TableBody>
        </Table>
      </TableContainer>
    );
  }
  HopTable.propTypes = {
    data: PropTypes.object.isRequired
  };

  function YeastTable(props) {
    const classes = useStyles();
  
    return (
      <TableContainer component={Paper}>
        <Table className={classes.table} size="small" aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell >Temperature (&deg;C)</TableCell>
              <TableCell >Flocculation</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
              {props.data.yeasts.map((yeast, index) =>(
              <TableRow key={index}>
                <TableCell > {yeast.name} </TableCell>
                <TableCell >{(Math.round(yeast.min_temperature) + " to " + Math.round(yeast.max_temperature))}</TableCell>
                <TableCell >{yeast.flocculation}</TableCell>
              </TableRow>
              ))}
          </TableBody>
        </Table>
      </TableContainer>
    );
  }
  YeastTable.propTypes = {
    data: PropTypes.object.isRequired
  };

  function MashTable(props) {
    const classes = useStyles();
  
    return (
      <TableContainer component={Paper}>
        <Table className={classes.table} size="small" aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>Step</TableCell>
              <TableCell>Amount (L)</TableCell>
              <TableCell >Type</TableCell>
              <TableCell >Temperature (&deg;C)</TableCell>
              <TableCell >Time (mins)</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
              {props.data.mash.mash_steps.map((mash, index) =>(
              <TableRow key={index}>
                <TableCell > {mash.name} </TableCell>
                <TableCell >{mash.infuse_amount ? mash.infuse_amount.toFixed(2) : ""}</TableCell>
                <TableCell >{mash.type}</TableCell>
                <TableCell >{Math.round(mash.step_temp)}</TableCell>
                <TableCell >{Math.round(mash.step_time)}</TableCell>
              </TableRow>
              ))}
          </TableBody>
        </Table>
      </TableContainer>
    );
  }
  MashTable.propTypes = {
    data: PropTypes.object.isRequired
  };

export default function RecipeCard(props) {
  const classes = useStyles();
  const [expanded, setExpanded] = React.useState(false);
  const [favourite, setFavourite] = React.useState(false);
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  const handleFavouriteClick = () => {
    setFavourite(!favourite);
  };

  const handleMenuClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleMenuDelete = () => {
      var endpointStr = "api/recipes/Recipe/".concat(props.data.id)
        setTimeout(() => {
        fetch(endpointStr, {
          method: 'DELETE',
          body: "",
          headers: { 'Content-Type': 'application/json' }
        })
          .catch(error => console.error('Error:', error))
          .then(response => {console.log('Success:', response);
          props.onChange();
        })
      }, 400);
    setAnchorEl(null);
  };
  
  return (
    <Card className={classes.root}>
        <Menu
            id="simple-menu"
            anchorEl={anchorEl}
            keepMounted
            open={Boolean(anchorEl)}
            onClose={handleMenuClose}
        >
            <MenuItem onClick={handleMenuClose}>Edit</MenuItem>
            <MenuItem onClick={handleMenuDelete}>Delete</MenuItem>
        </Menu>
      <CardHeader
        action={
          <IconButton  aria-controls="simple-menu" aria-haspopup="true"  onClick={handleMenuClick}>
            <MoreVertIcon />
          </IconButton>
        }
        title={props.data.id + " - " + props.data.name}
        subheader={props.data.style.name}
      />
      <CardContent>
      <Grid container className={classes.root} spacing={2}>
            <Grid item xs={12}>
        {InfoTable(props)}
        </Grid>
        <Grid item xs={12}>
        <Typography variant="h3" component="p">
          Brewers Notes
        </Typography>
        <Typography variant="body2" color="textSecondary" component="p">
          {props.data.notes}
        </Typography>
        </Grid>
        </Grid>
      </CardContent>

      <CardActions disableSpacing>
        <IconButton aria-label="add to favorites" onClick={handleFavouriteClick}>
          {favourite ? <StarIcon /> : <StarBorderIcon/>}
        </IconButton>
        <IconButton aria-label="share">
          <FaBeer />
        </IconButton>
        <IconButton
          className={clsx(classes.expand, {
            [classes.expandOpen]: expanded,
          })}
          onClick={handleExpandClick}
          aria-expanded={expanded}
          aria-label="show more"
        >
          <ExpandMoreIcon />
        </IconButton>
      </CardActions>

      <Collapse in={expanded} timeout="auto" unmountOnExit>
        <CardContent>
        <Grid container className={classes.root} spacing={2}>
            <Grid item xs={12}>
        <Typography variant="h3" component="p">
          Fermentables
        </Typography>
          {FermentableTable(props)}
          </Grid>
          <Grid item xs={12}>
          <Typography variant="h3" component="p">
          Hops
        </Typography>
          {HopTable(props)}
          </Grid>
          <Grid item xs={12}>
          <Typography variant="h3" component="p">
          Yeasts
        </Typography>
          {YeastTable(props)}
          </Grid>
          <Grid item xs={12}>
          <Typography variant="h3" component="p">
          Mash Steps
        </Typography>
          {MashTable(props)}
          </Grid>
          </Grid>
        </CardContent>
      </Collapse>
    </Card>
  );
}
RecipeCard.propTypes = {
    data: PropTypes.object.isRequired,
    onChange: PropTypes.func.isRequired
};