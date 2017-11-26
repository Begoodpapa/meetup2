/**
 * Built-in Log Configuration
 * (sails.config.log)
 *
 * Configure the log level for your app, as well as the transport
 * (Underneath the covers, Sails uses Winston for logging, which
 * allows for some pretty neat custom transports/adapters for log messages)
 *
 * For more information on the Sails logger, check out:
 * http://sailsjs.org/#!/documentation/concepts/Logging
 */
   var sails = require('sails');
   var winston = require('winston');
   var customerLogger = new winston.Logger();
   var sails_log_level = 'error';
   customerLogger.add(winston.transports.Console, {
    level: sails_log_level,
    colorize: true
   });

   customerLogger.add(winston.transports.File, {
    level: sails_log_level,
    filename: 'test_log.log',
    colorize: true,
    json: true
   });

module.exports.log = {

  /***************************************************************************
  *                                                                          *
  * Valid `level` configs: i.e. the minimum log level to capture with        *
  * sails.log.*()                                                            *
  *                                                                          *
  * The order of precedence for log levels from lowest to highest is:        *
  * silly, verbose, info, debug, warn, error                                 *
  *                                                                          *
  * You may also set the level to "silent" to suppress all logs.             *
  *                                                                          *
  ***************************************************************************/
   custom: customerLogger,
   level: 'error',
   inspect: false

};
