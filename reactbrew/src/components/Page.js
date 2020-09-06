import React, { forwardRef } from 'react';
import { Helmet } from 'react-helmet';
import PropTypes from 'prop-types';

const Page = forwardRef(({
  children,
  title = '',
  ...rest
}, ref) => {
  return (
    <div
      ref={ref}
      {...rest}
    >
      <Helmet 
        defaultTitle="M&H BrewCo."
        titleTemplate="M&H BrewCo. - %s"
      >
        <title>{title}</title>
        <html lang='en' />
        <meta name="description" content="M&H BrewCo. Brew Controller" />
        <noscript>You need to enable JavaScript to run this app.</noscript>
      </Helmet>
      {children}
    </div>
  );
});

Page.propTypes = {
  children: PropTypes.node.isRequired,
  title: PropTypes.string
};

export default Page;
