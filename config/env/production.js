/**
 * Production environment settings
 *
 * This file can include shared settings for a production environment,
 * such as API keys or remote database passwords.  If you're using
 * a version control solution for your Sails app, this file will
 * be committed to your repository unless you add it to your .gitignore
 * file.  If your repository will be publicly viewable, don't add
 * any private information to this file!
 *
 */

module.exports = {

  /***************************************************************************
   * Set the default database connection for models in the production        *
   * environment (see config/connections.js and config/models.js )           *
   ***************************************************************************/

  models: {
    connection: 'mysql'
  },

  /***************************************************************************
   * Set the port in the production environment to 80                        *
   ***************************************************************************/

  port: process.env.MEETUP_PORT || 1339,

  /***************************************************************************
   * Set the log level in production environment to "silent"                 *
   ***************************************************************************/

  // log: {
  //   level: "silent"
  // }

  blueprints: {
    actions: false,
    shortcuts: false,
    populate: false,
    rest: false
  },

  session: {
    secret: '5d939dc3d713d8532c1545bde818a665',
    adapter: 'redis',
  },

  assetsdir: {
    directory: '/prodassets'
  },

  persona: {
    server: 'http://beehive.eecloud.dynamic.nsn-net.net:1338'
  },

  pigeon: {
    server: 'http://beehive.eecloud.dynamic.nsn-net.net:1342'
  },


};