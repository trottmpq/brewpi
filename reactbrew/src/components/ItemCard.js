import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Backdrop from '@material-ui/core/Backdrop';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardHeader from '@material-ui/core/CardHeader';
import CardContent from '@material-ui/core/CardContent';
import Divider from '@material-ui/core/Divider';
import Modal from '@material-ui/core/Modal';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/styles';
import ItemCardUpdate from 'src/components/ItemCardUpdate';

const styles = theme => ({
  modal: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  },
  paper: {
    backgroundColor: theme.palette.background.paper,
    border: '0px solid #000',
    boxShadow: theme.shadows[5],
    padding: theme.spacing(2, 4, 3)
  }
});

class ItemCard extends Component {
  state = { show: false };

  showModal = () => {
    this.setState({ show: true });
  };

  hideModal = () => {
    this.setState({ show: false });
  };

  render() {
    const { classes } = this.props;

    console.log(this.props.data);
    return (
      <Card>
        <CardActionArea onClick={this.showModal}>
          <CardHeader title={this.props.data.name} />
          <Divider />
          <CardContent>
            {Object.keys(this.props.data).map((key, i) => (
              <Typography color="textSecondary" key={i}>
                {key}:{' '}
                {this.props.data[key] === null
                  ? 'Unkown'
                  : this.props.data[key].toString()}
              </Typography>
            ))}
          </CardContent>
        </CardActionArea>
        <Modal
          aria-labelledby="transition-modal-title"
          aria-describedby="transition-modal-description"
          className={classes.modal}
          open={this.state.show}
          onClose={this.hideModal}
          closeAfterTransition
          BackdropComponent={Backdrop}
          BackdropProps={{
            timeout: 500
          }}
        >
          <ItemCardUpdate type={this.props.type} handleClose={this.hideModal} data={this.props.data}/>
        </Modal>
      </Card>
    );
  }
}

ItemCard.propTypes = {
  type: PropTypes.string.isRequired,
  data: PropTypes.object.isRequired
};

export default withStyles(styles)(ItemCard);
