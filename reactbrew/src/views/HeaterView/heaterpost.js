import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import Modal from '@material-ui/core/Modal';
import Backdrop from '@material-ui/core/Backdrop';
import Fade from '@material-ui/core/Fade';
import Fab from '@material-ui/core/Fab';
import AddIcon from '@material-ui/icons/Add';

const useStyles = makeStyles(theme => ({
  modal: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  },
  paper: {
    backgroundColor: theme.palette.background.paper,
    border: '2px solid #000',
    boxShadow: theme.shadows[5],
    padding: theme.spacing(2, 4, 3)
  },
  fab: {
    margin: 0,
    top: 'auto',
    left: 'auto',
    bottom: 20,
    right: 20,
    position: 'fixed'
  }
}));

export default function HeaterForm() {
  const classes = useStyles();
  const [open, setOpen] = React.useState(false);

  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <div>
      <Fab
        color="primary"
        aria-label="add"
        className={classes.fab}
        onClick={handleOpen}
      >
        <AddIcon />
      </Fab>
      <Modal
        aria-labelledby="transition-modal-title"
        aria-describedby="transition-modal-description"
        className={classes.modal}
        open={open}
        onClose={handleClose}
        closeAfterTransition
        BackdropComponent={Backdrop}
        BackdropProps={{
          timeout: 500
        }}
      >
        <Fade in={open}>
          <Paper>
            <form>
            <Typography variant="h1" component="h2">
            Add Heater
          </Typography>
              <List>
                <ListItem alignItems="center">
                  <Typography color="textSecondary" align-items="flex-end">
                    Name:
                    <TextField
                      id="outlined-basic"
                      label="Name"
                      variant="outlined"
                    />
                  </Typography>
                </ListItem>
                <ListItem>
                  <Typography color="textSecondary">
                    GPIO Number:
                    <TextField
                      id="outlined-basic"
                      label="GPIO Number"
                      variant="outlined"
                    />
                  </Typography>
                </ListItem>
                <ListItem>
                  {' '}
                  <Button
                    variant="contained"
                    color="primary"
                    type="submit"
                    value="Submit"
                  >
                    Submit
                  </Button>
                </ListItem>
              </List>
            </form>
          </Paper>
        </Fade>
      </Modal>
    </div>
  );
}
