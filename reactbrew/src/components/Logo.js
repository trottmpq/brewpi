import React from 'react';

const Logo = props => {
  return (
    <img
      alt="Logo"
      src={process.env.PUBLIC_URL + '/static/frog.svg'}
      width="40"
      height="40"
      {...props}
    />
  );
};

export default Logo;
