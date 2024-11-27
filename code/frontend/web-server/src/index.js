/* Default webserver */
/* eslint no-console: ["error", { allow: ["warn", "error"] }] */

const app = require('./app');

const port = '8888';

app.listen(port, () => {
  console.log(`Server is listening on port ${port}...`);
});