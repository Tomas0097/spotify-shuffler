const path = require('path');

module.exports = {
  mode: 'development',
  watch: true,
  entry: './web/static/src/js/main.js',
  output: {
    filename: 'build.js',
    path: path.resolve(__dirname, 'web/static/dist/js'),
  },
};