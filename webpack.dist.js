var webpack = require('webpack');
var CommonsChunkPlugin = require("webpack/lib/optimize/CommonsChunkPlugin");
const DefinePlugin = webpack.DefinePlugin;
const HotModuleReplacementPlugin = webpack.HotModuleReplacementPlugin;
// const HtmlWebpackPlugin = require('html-webpack-plugin');
const NoErrorsPlugin = webpack.NoErrorsPlugin;
const OccurenceOrderPlugin = webpack.optimize.OccurenceOrderPlugin;


const path = require('path');

module.exports = {
  entry: [
    './react/main.js',
  
  ],
  output: {
    filename: 'bundle.js',
    path: path.resolve('./assets/js'),
    publicPath: '/'
  },
  resolve: {
    extensions: ['', '.js', '.jsx'],
    root: path.resolve('./react') //set root folder
  },
  module: {
    loaders:[
      { 
        test: /\.js[x]?$/, 
        loader: 'babel',
        exclude:/node_modules/, 
        query: {
          presets: ['es2015', 'react','stage-0' ]
        }
      },
      {
        test: /\.css$/, // Only .css files
        loader: 'style!css' // Run both loaders
      },
      {test: /\.(jpg|png|jpeg|gif)$/, loader: 'file'
      },
      {test: /\.eot/,loader : 'file?prefix=font/'},
      {test: /\.woff/,loader : 'file?prefix=font/&limit=10000&mimetype=application/font-woff'},
      {test: /\.ttf/, loader : 'file?prefix=font/'}, 
      {test: /\.svg/, loader : 'file?prefix=font/'} 	  
    ]
  },
  plugins: [
    new DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify('production')
    }),
  ] ,

}
