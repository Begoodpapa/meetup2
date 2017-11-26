'use strict';
var Promise = require("bluebird");
var _ = require('lodash');

var DEFAULT_ROLES = [
  {
    name:'administrator',
    scope:'global',
    privileges: {
      deletegroup:'yes',
      editgroup:'yes',
      addgroupmember:'yes',
      deletegroupmember:'yes',
      exportgroupmember:'yes',
      uploadpaper:'yes',
      deletepaper:'yes',
      gettestreport:'yes',
      createtag:'yes',
      deletetag:'yes',
      deletefile:'yes',
      deletetest: 'yes',
      deleteevent:'yes',
      editevent:'yes',
      publishevent:'yes',
      addeventmember:'yes',
      deleteeventmember:'yes',
      exporteventmember:'yes',
      admincontrol:'yes'
    }
  },

  {
    name: 'groupowner',
    scope:'group',
    privileges: {
      deletegroup:'yes',
      editgroup:'yes',
      addgroupmember:'yes',
      deletegroupmember:'yes',
      exportgroupmember:'yes',
      uploadpaper:'yes',
      deletepaper:'yes',
      gettestreport:'yes',
      createtag:'yes',
      deletetag:'yes',
      deletefile:'yes',
      deletetest: 'yes',
      deleteevent:'yes',
      publishevent:'yes',
      editevent:'yes',
      addeventmember:'yes',
      deleteeventmember:'yes',
      exporteventmember:'yes',
      admincontrol:'no'
    }
  },

  {
    name: 'eventowner',
    scope:'event',
    privileges: {
      deletegroup:'no',
      editgroup:'no',
      addgroupmember:'no',
      deletegroupmember:'no',
      exportgroupmember:'no',
      uploadpaper:'no',
      deletepaper:'no',
      gettestreport:'no',
      createtag:'no',
      deletetag:'no',
      deletefile:'no',
      deletetest:'no',
      deleteevent:'yes',
      editevent:'yes',
      publishevent:'yes',
      addeventmember:'yes',
      deleteeventmember:'yes',
      exporteventmember:'yes',
      admincontrol:'no'
    }
  }

];


module.exports = {

  assignPrivilege: function (userid, role, scope, targetid, cb) {

    Privilege.find({userid: userid, scope: scope, targetid: targetid })
    .then(function(found){
      if(found.length>0){ throw('user has been assigned relevant privilege in scope:'+ scope + ' targetid:'+ targetid);}

      var newPrivilege = {};
      newPrivilege.userid = userid;
      newPrivilege.scope = scope;
      newPrivilege.targetid = targetid;
      newPrivilege.role = role;
      return Privilege.create(newPrivilege);
    })
    .then(function(createdPrivilege){
      cb(null, createdPrivilege);
    })
    .catch(function(err){
      cb(err);
    });
  },

  updatePrivilegeByRole: function(privilege, newRole, cb){
    Privilege.update(privilege.id, {role: newRole,})
    .then(function(updated){
      console.log(updated);
      if(updated.length>0){
        cb(null, updated[0]);
      }else{
        cb('no privilege record was updated', null);
      }
    })
    .catch(function(err){
      cb(err,null);
    })
  },


  getRolesByScope: function(scope, cb){
    Role.find({scope:scope},cb);
  },

  getPrivilege: function(userid, scope, targetid, cb){
    Privilege.find({userid: userid, scope: scope, targetid: targetid}, cb);
  },

  getPrivilegeUserListByRole: function (role, scope, targetid, cb) {
    async.waterfall([

      function(callback){
        Privilege.find({role: role, scope: scope, targetid: targetid,}, callback);
      },

      function(privilegeList, callback){
        async.map(privilegeList, function(privilegeItem, cb){
          User.findOne({id: privilegeItem.userid}, cb);
        }, callback);
      },

    ], function (err, userlist) {
      if(err){
        cb(err, null);
      }else{
        var roleItem = {};
        roleItem.role = role;
        roleItem.userlist = userlist;
        cb(null, roleItem);
      }
    });
  },


  initPrivileges: function(cb){

    var roleObj;

    async.map(DEFAULT_ROLES, function(role, cb){
      roleObj = {};
      roleObj.name = role.name;
      roleObj.scope = role.scope;
      roleObj.isDefaultRole = 'yes';
      _.assign(roleObj, role.privileges);
      Role.findOrCreate({name: roleObj.name,}, roleObj, cb)
    }, function(err, results){
      if(err){
        cb(err);
      }else{
        cb(null);
      }
    });
  },

}
