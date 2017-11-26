'use strict';

module.exports = {

  auth: function(uid, password, callback) {
    User.findOne({
      uid: uid
    }, function(err, user) {
      if (user) {
        LDAPUtils.auth(user.dn, password, function(error) {
          if (error && sails.config.environment!=='development') {
            sails.log.error('LDAP auth:', error.message);
            callback(error);
          }else{
            callback(null, user);
          }
        });
      } else {
        LDAPUtils.fuzzySearch(uid, function(err, entry) {
          if (err) {
            callback(err);
          }else{
            User.create({
              uid: entry.uid,
              dn: entry.dn,
              fullname: entry.gecos,
              email: entry.mail,
              id: entry.dn.substr(15,8)
            }, function(err, createdUser) {
              if (err) {
                callback(err);
              }else{
                LDAPUtils.auth(entry.dn, password,
                  function(err) {
                    if (err  && sails.config.environment!=='development') {
                      sails.log.error('LDAP auth:', err.message);
                      callback(err);
                    }else{
                      callback(null, createdUser);
                    }
                  });
              }
            });
          }
        });
      }
    });
  }
};
