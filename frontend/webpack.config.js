var path = require('path');
var webpack = require('webpack');

module.exports = {
    entry: './src/main.js',
    output: {
        path: path.resolve(__dirname, './dist'),
        publicPath: '/dist/',
        filename: 'build.js'
    },
    resolve: {
        extensions: ['', '.js'],
        fallback: [path.join(__dirname, 'node_modules')],
        alias: {
            'src': path.resolve(__dirname, './src')
        }
    },
    resolveLoader: {root: path.join(__dirname, 'node_modules'),},
    module: {
        loaders: [
            {test: /\.js$/, loader: ['ng-annotate', 'babel-loader'], exclude: /node_modules/},
            {test: /\.html$/, loader: 'raw-loader'},
            {test: /\.css$/, loaders: ["style-loader", "css-loader"]},
            {test: /\.scss$/, loaders: ["style-loader", "css-loader", "sass-loader"]},
            {
                test: /\.(png|jpg|gif|svg|woff2?|eot|ttf)(\?.*)?$/,
                loader: 'url',
                query: {limit: 10000, name: '[name].[ext]?[hash:7]'}
            }

        ]
    },
    plugins: [
        new webpack.ProvidePlugin({
            $: "jquery",
            jQuery: "jquery",
            'window.jQuery': "jquery",
        })
    ]
};

if (process.env.NODE_ENV === 'production') {
    module.exports.devtool = 'source-map';
    module.exports.plugins = (module.exports.plugins || []).concat([
        new webpack.DefinePlugin({'process.env': {NODE_ENV: '"production"'}}),
        new webpack.optimize.UglifyJsPlugin({compress: {warnings: false}}),
        new webpack.optimize.OccurenceOrderPlugin()
    ])
}
