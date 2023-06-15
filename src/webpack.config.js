const path = require('path');

module.exports = {
  mode: 'development',
  entry: './web/static/src/js/main.js',
  output: {
    filename: 'build.js',
    path: path.resolve(__dirname, 'web/static/dist/js'),
  },
};