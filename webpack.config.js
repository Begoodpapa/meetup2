var webpack = require('webpack');
var CommonsChunkPlugin = require("webpack/lib/optimize/CommonsChunkPlugin");
const DefinePlugin = webpack.DefinePlugin;
const HotModuleReplacementPlugin = webpack.HotModuleReplacementPlugin;
//const HtmlWebpackPlugin = require('html-webpack-plugin');
const NoErrorsPlugin = webpack.NoErrorsPlugin;
const OccurenceOrderPlugin = webpack.optimize.OccurenceOrderPlugin;


const path = require('path');

module.exports = {
  entry: [
    'webpack-dev-server/client?http://0.0.0.0:8081/', // WebpackDevServer host and port
    'webpack/hot/only-dev-server', // "only" prevents reload on syntax errors
    './react/main.js',
  
  ],
  devtool: process.env.WEBPACK_DEVTOOL || 'source-map',
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
          presets: ['es2015', 'react','stage-0' ],
          plugins: [
            ['react-transform', {
              transforms: [{
                transform: 'react-transform-hmr',
                imports: ['react'],
                locals: ['module']
              }]
            }]
          ]
        }
      },
      {
        test: /\.css$/, // Only .css files
        loader: 'style!css' // Run both loaders
      },
      {test: /\.(jpg|png|jpeg|gif)$/, loader: 'file'},
      {test: /\.eot/,loader : 'file?prefix=font/'},
      {test: /\.woff/,loader : 'file?prefix=font/&limit=10000&mimetype=application/font-woff'},
      {test: /\.ttf/, loader : 'file?prefix=font/'}, 
      {test: /\.svg/, loader : 'file?prefix=font/'} 	  
    ]
  },
  plugins: [
    new webpack.HotModuleReplacementPlugin(),
    new HotModuleReplacementPlugin(),
  ] ,


  devServer: {
    contentBase: './react',
    historyApiFallback: true,
    hot: true,
    port: 8081,
    progress: true,
    publicPath: '/',
    stats: {
      cached: true,
      cachedAssets: true,
      chunks: true,
      chunkModules: false,
      colors: true,
      hash: false,
      reasons: true,
      timings: true,
      version: false
    }
  }

}
