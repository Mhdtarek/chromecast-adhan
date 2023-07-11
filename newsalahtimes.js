const util = require('util');
const exec = util.promisify(require('child_process').exec);

/*

var minutes = 1, the_interval = minutes * 60 * 1000;
setInterval(function() {
  execcmd(`catt -d kok cast_site "https://salattimes.com/place/295529600/salat-times/?language=arabic"`)
}, the_interval);
*/
execcmd(`catt cast_site "https://salattimes.com/place/295529600/salat-times/?language=arabic"`)


async function execcmd(command) {
  const { stdout, stderr } = await exec(command);
  console.log('stdout:', stdout);
  console.log('stderr:', stderr);
}
