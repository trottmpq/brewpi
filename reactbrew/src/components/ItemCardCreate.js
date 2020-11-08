import React, { Component } from 'react';
import { withStyles } from '@material-ui/core/styles';
import PropTypes from 'prop-types';
import Box from '@material-ui/core/Box';
import Button from '@material-ui/core/Button';
import Container from '@material-ui/core/Container';
import Divider from '@material-ui/core/Divider';
import Paper from '@material-ui/core/Paper';
import TextField from '@material-ui/core/TextField';
import Typography from '@material-ui/core/Typography';
import { Formik } from 'formik';
import * as Yup from 'yup';
import Fab from '@material-ui/core/Fab';
import AddIcon from '@material-ui/icons/Add';

const styles = theme => ({
  paper: {
    backgroundColor: theme.palette.background.paper,
    border: '0px solid #000',
    boxShadow: theme.shadows[5],
    padding: theme.spacing(2, 4, 3)
  }
});

class ItemCardUpdate extends Component {
  close = () => {
    // this.props.handleClose();
  };

  render() {
    const { classes } = this.props;

    return (
      <div>
        
        <Paper className={classes.paper}>
          <Container maxWidth="sm">
            <Formik
              initialValues={{ name: "New Name", gpio_num: 0}}
              validationSchema={Yup.object().shape({
                name: Yup.string()
                  .max(255)
                  .required('Name is required'),
                gpio_num: Yup.number()
                  .integer()
                  .required('GPIO Number is required'),
                  kettle_id: Yup.number()
                    .integer()
              })}
              onSubmit={(values, { setSubmitting }) => {
                console.log("Creating")
                console.log(this.props.URL)

                setTimeout(() => {
                  fetch(this.props.URL, {
                    method: 'POST',
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
                      Create Item
                    </Typography>
                    <Typography
                      color="textSecondary"
                      gutterBottom
                      variant="body2"
                    >
                      Use this Form to create this item.
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
                  <TextField
                    type="number"
                    name="gpio_num"
                    onChange={handleChange}
                    onBlur={handleBlur}
                    value={values.gpio_num}
                    error={Boolean(touched.gpio_num && errors.gpio_num)}
                    fullWidth
                    helperText={touched.gpio_num && errors.gpio_num}
                    label="GPIO Number"
                    margin="normal"
                    variant="outlined"
                  />
                  <TextField
                    type="number"
                    name="kettle_id"
                    onChange={handleChange}
                    onBlur={handleBlur}
                    value={values.kettle_id}
                    error={Boolean(touched.kettle_id && errors.kettle_id)}
                    fullWidth
                    helperText={touched.kettle_id && errors.kettle_id}
                    label="Kettle ID"
                    margin="normal"
                    variant="outlined"
                  />

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
ItemCardUpdate.propTypes = {
  URL : PropTypes.object.isRequired,
  handleClose: PropTypes.object.isRequired
};
export default withStyles(styles)(ItemCardUpdate);
