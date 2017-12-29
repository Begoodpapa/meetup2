'use strict';

var _request = require('request');

var request = _request.defaults({
  headers: {
    'Content-Type': 'application/json',
  }
});


module.exports = {

  sendNotifyMail: function(mailObj, cb){

    request.post(sails.config.pigeon.server+'/mail/', {
      json: {
        mailobj: mailObj
      }}, function(err, res, body){
        if(cb){
          cb(err, res, body);
        }
    });

  },

};
