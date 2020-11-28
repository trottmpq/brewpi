import React, { useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import PropTypes from 'prop-types';
import { Box, Drawer, Hidden, List, makeStyles } from '@material-ui/core';
import { FaBeer } from 'react-icons/fa';
import { RiTempColdLine } from 'react-icons/ri';
import { GiHeatHaze, GiCookingPot, GiWaterDrop } from 'react-icons/gi';
import NavItem from './NavItem';
import BallotIcon from '@material-ui/icons/Ballot';
const items = [
  {
    href: '/',
    icon: FaBeer,
    title: 'Home'
  },
  {
    href: '/kettles',
    icon: GiCookingPot,
    title: 'Kettles'
  },
  {
    href: '/tempsensors',
    icon: RiTempColdLine,
    title: 'Temp Sensors'
  },
  {
    href: '/heaters',
    icon: GiHeatHaze,
    title: 'Heaters'
  },
  {
    href: '/pumps',
    icon: GiWaterDrop,
    title: 'Pumps'
  },
  {
    href: '/recipes',
    icon: BallotIcon,
    title: 'Recipes'
  }
];

const useStyles = makeStyles(() => ({
  mobileDrawer: {
    width: 256
  },
  desktopDrawer: {
    width: 256,
    top: 64,
    height: 'calc(100% - 64px)'
  },
  avatar: {
    cursor: 'pointer',
    width: 64,
    height: 64
  }
}));

const NavBar = ({ onMobileClose, openMobile }) => {
  const classes = useStyles();
  const location = useLocation();

  useEffect(() => {
    if (openMobile && onMobileClose) {
      onMobileClose();
    }
  }, [location.pathname]);

  const content = (
    <Box height="100%" display="flex" flexDirection="column">
      <Box p={2}>
        <List>
          {items.map(item => (
            <NavItem
              href={item.href}
              key={item.title}
              title={item.title}
              icon={item.icon}
            />
          ))}
        </List>
      </Box>
    </Box>
  );

  return (
    <>
      <Hidden lgUp>
        <Drawer
          anchor="left"
          classes={{ paper: classes.mobileDrawer }}
          onClose={onMobileClose}
          open={openMobile}
          variant="temporary"
        >
          {content}
        </Drawer>
      </Hidden>
      <Hidden mdDown>
        <Drawer
          anchor="left"
          classes={{ paper: classes.desktopDrawer }}
          open
          variant="persistent"
        >
          {content}
        </Drawer>
      </Hidden>
    </>
  );
};

NavBar.propTypes = {
  onMobileClose: PropTypes.func,
  openMobile: PropTypes.bool
};

NavBar.defaultProps = {
  onMobileClose: () => {},
  openMobile: false
};

export default NavBar;
