#!/bin/bash
source ~/.profile 
source $BREWPI/../env/bin/activate
cd $BREWPI
source ~/.nvm/nvm.sh
nvm use 12
yarn start
