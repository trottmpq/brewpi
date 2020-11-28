import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Container, Typography } from '@material-ui/core';
import { withStyles } from '@material-ui/styles';
import Page from 'src/components/Page';
import Fab from '@material-ui/core/Fab';
import AddIcon from '@material-ui/icons/Add';
import RecipeCard from 'src/components/RecipeCard';
import { Grid } from '@material-ui/core';


const styles = theme => ({
  root: {
    backgroundColor: theme.palette.background.dark,
    minHeight: '100%',
    paddingBottom: theme.spacing(3),
    paddingTop: theme.spacing(3)
  },
  fab: {
    margin: 0,
    top: 'auto',
    left: 'auto',
    bottom: 20,
    right: 20,
    position: 'fixed'
  }
});

class Recipe extends Component {
  state = { recipelist : []}

  componentDidMount() {
    this.getapi = this.getapi.bind(this);
    this.getapi()
  }
  openCreate = () => {
    console.log("Opening create dialog")
    this.setState({createOpen: true})
  }

  closeCreate = () => {
    console.log("Closing create dialog")
    this.setState({createOpen: false})
  }

  getapi() {
    fetch("api/recipes/Recipe/")
      .then(res => res.json())
      .then(data => {
        this.setState({ recipelist: data });
        // console.log(data[0].name)
      })
      .catch(console.log);
  }

  onChangeHandler=event=>{
    console.log(event.target.files[0].name)
    event.preventDefault()
    const reader = new FileReader()
    reader.onload = async (event) => { 
      const text = (event.target.result)
      var values = {"xml" : text}
      console.log(values)
      setTimeout(() => {
        fetch("api/recipes/Recipe/", {
          method: 'POST',
          body: JSON.stringify(values, null, 2),
          headers: { 'Content-Type': 'application/json' }
        })
          .then(res => res.json())
          .catch(error => console.error('Error:', error))
          .then(response => {console.log('Success:', response);
          this.getapi();});
      }, 400);
      
    };
    reader.readAsText(event.target.files[0])
  }
      
  render() {
    const { classes } = this.props;
    return (
      <Page className={classes.root} title="Recipes">
        <Container maxWidth={false}>
          <Typography variant="h1" component="h2">
            Recipes 
          </Typography>
          <input type="file" name="file" onChange={(e) => this.onChangeHandler(e)} />
          <Grid container spacing={3}>
            {this.state.recipelist.map(data => (
            <Grid item lg={12} sm={12} xl={12} xs={12} key={data.id}>
              <RecipeCard data={data} onChange={this.getapi}/>
            </Grid>
          ))}
        </Grid>
        </Container>

        <Fab
        color="secondary"
        aria-label="add"
        className={classes.fab}
        onClick={this.openCreate}
      ><AddIcon />
      </Fab>
      </Page>
    );
  }
}
Recipe.propTypes = {
  classes: PropTypes.object.isRequired
};

export default withStyles(styles)(Recipe);
