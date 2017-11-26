'use strict';

var ldap = require('ldapjs');

var noop = function() {};

var createSearchOpt = function(uid){

  var reUidNumber = /^[1-9]\d{7}$/;
  var reUidMail = /[\w.]+@nokia.com$/;
  var filter = '';

  if (reUidNumber.test(uid)===true) {
    filter = 'uidNumber='+uid;
  }
  else if(reUidMail.test(uid)===true){
    filter = 'mail='+uid;
  }
  else{
    filter = 'uid='+uid;
  }
  
  return {
    filter: filter,
    scope: 'sub'
  };

};

module.exports = {

  auth: function(dn, password, callback) {
    callback = callback || noop;

    var client = ldap.createClient({
      url: sails.config.ldap.server
    });

    client.bind(dn, password, function(err) {
      client.unbind(function(unbinderr){
        if(unbinderr){
          console.log('ldap unbind err:', unbinderr);  
        }
      });
      return callback(err);
    });

  },

  fuzzySearch: function(uid, callback) {
    var client = ldap.createClient({
      url: sails.config.ldap.server
    });

    var opt = createSearchOpt(uid);

    callback = callback || noop;

    client.bind('', '', function(err) {
      if (err) {
        return callback(err);
      }

      client.search('', opt, function(err, response) {
        var entrys = [];
        if (err) {
          return callback(err);
        }

        response.on('searchEntry', function(entry) {
          entrys.push(entry.object);
        });

        response.on('end', function() {
          if (entrys.length === 0) {
            return callback(Error('NO SUCH uid: '+uid), null);
          }
          var entry = entrys[0];
          client.unbind(function(unbinderr){
            if(unbinderr){
              console.log('ldap unbind err:', unbinderr);  
            }
          });
          return callback(null, entry);
        });

        response.on('error', function(error) {
          console.log('xxerr',error.messsage);
          return callback(error);
        });
      });
    });

  }
};
