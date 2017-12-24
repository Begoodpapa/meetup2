'user strict';

var mailUtil = require('./mailUtil');

module.exports = {

  getGroupUsersMail: function(group_id, cb){
    var group_mail = [];
    var users;

    Group.find({id:group_id}).populate('user').exec(function(err, groups){
        if(err){
            if(cb && (typeof cb==='function')){
                cb(err,null);
            }
        }
        else{
            users = groups[0].user;
            var user_num = users.length;
            for(var i=0; i< user_num; i++){
                group_mail.push(users[i].email);    
            }
            if(cb && (typeof cb==='function')){
                cb(null, group_mail);
            }
        }
    });

  },

  findUserFromTheGroup: function(userid, groupid, cb){
    Group
      .find({
        id: groupid
      }).populate('user')
      .exec(function(err, groups) {
        if (err) {
          err = 'Failed to query database with groupid: ' + groupid;
          sails.log.error(err);
          return cb(err);
        } else {
          if (groups.length !== 0) {
            for (var i = 0; i < groups[0].user.length; i++) {
              if (userid === groups[0].user[i].id) {
                return cb(null, groups[0].user[i]);
              }
            }
            err = 'Could not find user in the group';
            return cb(Error(err));
          } else {
            err = 'The group is not existed';
            return cb(Error(err));
          }
        }
      });
  },


  add_user_to_group: function(user, groupid, cb) {

    Group
      .find({
        id: groupid
      }).populate('user')
      .exec(function(err, groups) {
        if (err) {
          err = 'Failed to query database with groupid: ' + groupid;
          sails.log.error(err);
          return cb(Error(err));

        } else {
          if (groups.length !== 0) {
            for (var i = 0; i < groups[0].user.length; i++) {
              if (user.id === groups[0].user[i].id) {
                //user existed in group already
                return cb(null, user);
              }
            }
            groups[0].user.add(user.id);
            groups[0].save(function(err, s) {
              if (err) {
                console.log('user was failed to add to group:', err);
                return cb(Error(err));
              } else {
                return cb(null, user);
              }

            });

          } else {
            err = 'Failed to find group with groupid:' + groupid;
            sails.log.error(err);
            return cb(Error(err));

          }

        }

      });

  },


  remove_user_from_group : function(user, groupid, cb) {

    Group
      .find({
        id: groupid
      }).populate('user')
      .exec(function(err, groups) {
        if (err) {
          err = 'Failed to query database with groupid: ' + groupid;
          sails.log.error(err);
          return cb(err);
        } else {
          if (groups.length !== 0) {
            for (var i = 0; i < groups[0].user.length; i++) {
              if (user.id === groups[0].user[i].id) {
                groups[0].user.remove(user.id);
                groups[0].save(function(err, s) {
                  if (err) {
                    err = 'Failed to remove user and save' + user.id;
                    sails.log.err(err);
                    return cb(Error(err));
                  } else {
                    return cb(err);
                  }
                });
              }
            }
          } else {
            err = 'The group is not existed';
            return cb(Error(err));
          }
        }
      });

  },


  sendNotifyMailToGroupUsers: function(group_id, mail_obj, cb){
    this.getGroupUsersMail(group_id, function(err, group_mail){
      if(err){
          if(cb && (typeof cb==='function')){
              cb(err);
          }
      }
      else{
          mail_obj.to = group_mail;
          mailUtil.sendNotifyMail(mail_obj, cb);
      }

    });
  },

};