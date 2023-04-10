#!/bin/bash

cd /opt/spotify-shuffler/src

# Installs necessary NodeJS packages for webpack.
npm install

# Runs webpack to compile frontend files + watching the file changes.
npm run build