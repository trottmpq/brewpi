import React from 'react';

const Logo = props => {
  return (
    <img
      alt="Logo"
      src={process.env.PUBLIC_URL + '/static/hopslogo.svg'}
      width="50"
      height="50"
      {...props}
    />
  );
};

export default Logo;
