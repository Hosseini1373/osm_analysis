const express = require('express');
const compression = require('compression');
var { createProxyMiddleware } = require('http-proxy-middleware');
const app = express();
const PORT = 3000;
const HOST="localhost"
const flask_server="http://localhost:5000"


app.use(compression());


// Proxy endpoints
app.use('/test', createProxyMiddleware({
	target: flask_server,
	secure:false,
	pathRewrite: {
		['^/test']: '/test',
	},
 }));

 app.get('/info', (req, res, next) => {
	res.send('This is a proxy service which proxies to flask server.');
 });

 var bServeDist = false;
// eslint-disable-next-line strict
process.argv.forEach(function (val, index, array) {
	if (val == '--dist') {
		bServeDist = true;
	}
});

if (bServeDist) {
	app.use(express.static('dist'));
} else {
	app.use('/', createProxyMiddleware('http://localhost:8080'));
}

 app.listen(PORT,() => {
	console.log('Starting Proxy at '+ PORT);
 });