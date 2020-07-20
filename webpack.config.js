var path = require('path')
var MiniCssExtractPlugin = require('mini-css-extract-plugin')
var TerserPlugin = require('terser-webpack-plugin')
var WebpackBundleTracker = require('webpack-bundle-tracker')

module.exports = {
  entry: {
    shop: './static/javascript/shop',
  },
  output: {
    filename: '[name]_[hash].js',
    path: path.resolve(__dirname, 'staticfiles/bundles'),
    publicPath: 'http://localhost:8080/static/bundles/',
  },
  devtool: 'inline-source-map',
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],
          }
        },
      },
      {
        test: /\.(sa|sc|c)ss$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
          },
          {
            loader: 'css-loader',
          },
          {
            loader: 'sass-loader',
            options: {
              implementation: require('sass'),
            }
          },
        ]
      },
      {
        test: /\.(png|jpe?g|gif|svg)$/,
        use: [
          {
            loader: 'file-loader',
          },
        ]
      },
    ]
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: '[name]_[hash].css',
    }),
    new WebpackBundleTracker({
      filename: './webpack-stats.json'
    }),
  ],
  optimization: {
    minimizer: [new TerserPlugin()],
  },
  mode: 'development',
}
