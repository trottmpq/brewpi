import { Component } from 'react';
import { withStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';
// import Box from '@material-ui/core/Box';
// import Button from '@material-ui/core/Button';
// import Container from '@material-ui/core/Container';
// import Divider from '@material-ui/core/Divider';
// import Paper from '@material-ui/core/Paper';
// import TextField from '@material-ui/core/TextField';
// import Typography from '@material-ui/core/Typography';
// import { Formik } from 'formik';
import * as Yup from 'yup';

const styles = theme => ({
  paper: {
    backgroundColor: theme.palette.background.paper,
    border: '0px solid #000',
    boxShadow: theme.shadows[5],
    padding: theme.spacing(2, 4, 3)
  }
});

class KettleCardUpdate extends Component {
  state = { createOpen: false}
  close = () => {
    this.props.handleClose();
  };
  deleteKettle = () => {
    console.log("Deleting")
    var baseStr = this.props.URL;
    var endpointStr = baseStr.concat(this.props.data.id)
    console.log(endpointStr)
    setTimeout(() => {
      fetch(endpointStr, {
        method: 'DELETE',
        body: "",
        headers: { 'Content-Type': 'application/json' }
      })
        .then(res => res.json())
        .catch(error => console.error('Error:', error))
        .then(response => console.log('Success:', response));

      this.close();
    }, 400);
  };
  render() {
    const { classes, data } = this.props;

    return (
      <div>
        <Paper className={classes.paper}>
          <Container maxWidth="sm">
            <Formik
              initialValues={{ name: data.name}}
              validationSchema={Yup.object().shape({
                name: Yup.string()
                  .max(255)
                  .required('Name is required')
              })}
              onSubmit={(values, { setSubmitting }) => {
                var baseStr = this.props.URL;
                var endpointStr = baseStr.concat(this.props.data.id)
                console.log(endpointStr)
                setTimeout(() => {
                  fetch(endpointStr, {
                    method: 'PUT',
                    body: JSON.stringify(values, null, 2),
                    headers: { 'Content-Type': 'application/json' }
                  })
                    .then(res => res.json())
                    .catch(error => console.error('Error:', error))
                    .then(response => console.log('Success:', response));
                  setSubmitting(false);
                  this.close();
                }, 400);
              }}
            >
              {({
                values,
                errors,
                touched,
                handleChange,
                handleBlur,
                handleSubmit,
                isSubmitting
                /* and other goodies */
              }) => (
                <form onSubmit={handleSubmit}>
                  <Box mb={3}>
                    <Typography color="textPrimary" variant="h2">
                      {this.props.data.name}
                    </Typography>
                    <Typography
                      color="textSecondary"
                      gutterBottom
                      variant="body2"
                    >
                      Use this Form to update this item.
                    </Typography>
                  </Box>
                  <Divider />
                  <TextField
                    type="text"
                    name="name"
                    onChange={handleChange}
                    onBlur={handleBlur}
                    value={values.name}
                    error={Boolean(touched.name && errors.name)}
                    fullWidth
                    helperText={touched.name && errors.name}
                    label="Name"
                    margin="normal"
                    variant="outlined"
                  />
                  <Box my={2}>
                  <Button 
                  disabled={isSubmitting}
                  fullWidth
                  size="large"
                  variant="outlined" 
                  onClick={this.close}>
                    Cancel</Button>
                  </Box>
                  <Box my={2}>
                  <Button 
                  disabled={isSubmitting}
                  fullWidth
                  size="large"
                  variant="outlined" 
                  onClick={this.deleteKettle}>
                    Delete</Button>
                  </Box>
                  <Box my={2}>
                    <Button
                      color="primary"
                      disabled={isSubmitting}
                      fullWidth
                      size="large"
                      type="submit"
                      variant="contained" 
                    >
                      Submit
                    </Button>
                  </Box>
                </form>
              )}
            </Formik>
          </Container>
        </Paper>
      </div>
    );
  }
}
KettleCardUpdate.propTypes = {
  URL : PropTypes.string.isRequired,
  data: PropTypes.object.isRequired,
  handleClose: PropTypes.func.isRequired
};
export default withStyles(styles)(KettleCardUpdate);
