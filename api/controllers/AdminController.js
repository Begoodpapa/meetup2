'use strict';
var privilegeUtil = require('../../lib/privilegeUtil.js');
var groupUtil = require('../../lib/groupUtil.js');
var eventUtil = require('../../lib/eventUtil.js');

module.exports = {

  showAdminDashboard: function(req, res){
    var user = req.session.user;
    return res.view('admin/adminIndex', {
      page: 'dashboard',
      user: user
    });
  },

  showAdminGlobalPrivilege: function(req, res){
    var user = req.session.user;
    var roleList = new Array();

    async.waterfall([

      function(callback){
        privilegeUtil.getRolesByScope('global', callback);
      },

      function(globalRoles, callback){
        async.map(globalRoles, function(role, cb){
          privilegeUtil.getPrivilegeUserListByRole(role.name,'global', null, cb);
        }, callback);
      },

    ], function(err, rolelist){

      if(err){
        sails.log.error(err);
        return res.negotiate(err);
      }else{
        return res.view('admin/adminIndex', {
          page: 'globalPrivilege',
          rolelist: rolelist,
          user: user
        });
      }

    });

  },

  showAdminGroupPrivilege: function(req, res){
    var user = req.session.user;
    var grouplist;


    async.waterfall([

      function(callback){
        Group.find({},callback);
      },

      function(groups, callback){
        grouplist = groups;
        privilegeUtil.getRolesByScope('group', callback);
      },

      function(roles, callback){
        callback(null, roles, grouplist);
      },

    ], function(err, roles, grouplist){

      if(err){
        sails.log.error(err);
        return res.negotiate(err);
      }else{
        return res.view('admin/adminIndex', {
          page: 'groupPrivilege',
          roles: roles,
          grouplist: grouplist,
          user: user
        });
      }

    });

  },

  showAdminSingleGroupPrivilege: function(req, res){
    var groupid= req.param('groupid');

    async.waterfall([

      function(callback){
        privilegeUtil.getRolesByScope('group', callback);
      },

      function(groupRoles, callback){
        async.map(groupRoles, function(role, cb){
          privilegeUtil.getPrivilegeUserListByRole(role.name, 'group', groupid,  cb);
        }, callback);
      },

    ], function(err, rolelist){

      if(err){
        return res.json(200, {error: err});
      }else{
        return res.json(200, {
          rolelist: rolelist,
        });
      }
    });

  },


  showAdminEventPrivilege: function(req, res){
    var user = req.session.user;
    var eventlist;

    async.waterfall([

      function(callback){
        Event.find({},callback);
      },

      function(events, callback){
        eventlist = events;
        privilegeUtil.getRolesByScope('event', callback);
      },

      function(roles, callback){
        callback(null, roles, eventlist);
      },

    ], function(err, roles, eventlist){

      if(err){
        sails.log.error(err);
        return res.negotiate(err);
      }else{
        return res.view('admin/adminIndex', {
          page: 'eventPrivilege',
          roles: roles,
          eventlist: eventlist,
          user: user
        });
      }

    });

  },

  showAdminSingleEventPrivilege: function(req, res){
    var eventid= req.param('eventid');

    async.waterfall([

      function(callback){
        privilegeUtil.getRolesByScope('event', callback);
      },

      function(eventRoles, callback){
        async.map(eventRoles, function(role, cb){
          privilegeUtil.getPrivilegeUserListByRole(role.name, 'event', eventid,  cb);
        }, callback);
      },

    ], function(err, rolelist){

      if(err){
        return res.json(200, {error: err});
      }else{
        return res.json(200, {
          rolelist: rolelist,
        });
      }
    });

  },


  updateGlobalPrivilege: function(req, res){

    var userid= req.param('userid');
    var role= req.param('role');

    async.waterfall([

      function(callback){
        User.find({id: userid}).exec(callback);
      },

      function(user, callback){
        if(user.length>0){
          privilegeUtil.getPrivilege(userid,'global', null, callback);
        }else{
          callback("User ID is not exist !");
        }
      },

      function(privilegeList, callback){
        if (privilegeList.length>0){
          privilegeUtil.updatePrivilegeByRole(privilegeList[0], role, callback);
        }else{
          privilegeUtil.assignPrivilege(userid, role, 'global', null, callback);
        }
      }

    ], function(err){
      if(err){
        return res.json(200, {error: err});
      }else{
        return res.json(200);
      }
    });

  },

  updateGroupPrivilege: function(req, res){

    var userid= req.param('userid');
    var groupid= req.param('groupid');
    var role= req.param('role');

    async.waterfall([

      function(callback){
        User.find({id: userid}).exec(callback);
      },

      function(user, callback){
        if(user.length>0){
          groupUtil.add_user_to_group(user[0], groupid, callback);
        }else{
          callback("User ID is not exist !");
        }
      },

      function(user, callback){
        if(user!==null){
          privilegeUtil.getPrivilege(userid, 'group', groupid, callback);
        }else{
          callback("User add Group fail !");
        }
      },

      function(privilegeList, callback){
        if (privilegeList.length>0){
          privilegeUtil.updatePrivilegeByRole(privilegeList[0], role, callback);
        }else{
          privilegeUtil.assignPrivilege(userid, role, 'group', groupid, callback);
        }
      }

    ], function(err){

      if(err){
        return res.json(200, {error: err});
      }else{
        return res.json(200);
      }
    });

  },

  updateEventPrivilege: function(req, res){

    var userid= req.param('userid');
    var eventid= req.param('eventid');
    var role= req.param('role');
    var user;

    async.waterfall([

      function(callback){
        User.find({id: userid}).exec(callback);
      },

      function(found, callback){
        if(found.length>0){
          user = found[0];
          Event.find({id: eventid}).exec(callback);
        }else{
          callback("User ID is not exist !");
        }
      },

      function(found, callback){
        if(found.length>0){
          groupUtil.add_user_to_group(user, found[0].group, callback);
        }else{
          callback("Event ID is not exist !");
        }
      },

      function(foundUser, callback){
        if(foundUser!==null){
          eventUtil.addOneUserToEvent(user, eventid, callback);
        }else{
          callback("User add Group fail !");
        }
      },

      function(foundUser, callback){
        if(foundUser!==null){
          privilegeUtil.getPrivilege(userid, 'event', eventid, callback);
        }else{
          callback("User add Event fail !");
        }
      },

      function(privilegeList, callback){
        if (privilegeList.length>0){
          privilegeUtil.updatePrivilegeByRole(privilegeList[0], role, callback);
        }else{
          privilegeUtil.assignPrivilege(userid, role, 'event', eventid, callback);
        }
      }

    ], function(err){

      if(err){
        return res.json(200, {error: err});
      }else{
        return res.json(200);
      }
    });

  },


  showAdminRoleManage: function(req, res){

    var user = req.session.user;

    Role.find({}, function(err, found){
      return res.view('admin/adminIndex', {
        page: 'roleManage',
        adminRoleList: found,
        user: user 
      });
    });
  },

  addOrUpdateAdminRole: function(req, res){
    var roleObj = req.param('roleObj');

    Role.find({name:roleObj.name},function(err, found){
      if(err){
        return res.json(200, {error: err});
      }else{
        if(found.length!=0){
          Role.update(found[0].id, roleObj, function(err, updated){
            if(err){
              return res.json(200, {error: err});
            }else{
              return res.json(200);
            }
          });
        }else{
          Role.create(roleObj,function(err, createdRole){
            if(err){
              return res.json(200, {error: err});
            }else{
              return res.json(200);
            }
          });
        }       
      }
    });
  },

  deleteAdminRole: function(req, res){
    var rolename = req.param('rolename');

    async.waterfall([

      function(callback){
        Privilege.find({role: rolename}, callback);
      },

      function(found, callback){
        if(found.length>0){
          callback("this role has been assigned to someone");
        }else{
          Role.find({name:rolename}, callback);
        }
      },

      function(found, callback){
        if(found.length>0){
          Role.destroy({id:found[0].id}, callback);
        }else{
          callback("couldn't find this role");
        }
      }

    ], function(err){

      if(err){
        return res.json(200, {error: err});
      }else{
        return res.json(200);
      }
    });

  },


  getAdminRoleDetail: function(req, res){
    var rolename = req.param('rolename');

    Role.find({name:rolename},function(err, found){
      if(err){
        return res.json(200, {error: err});
      }else{
        if(found.length>0){
          return res.json(200, {
            roleDetail: found[0],
          });
        }else{
          return res.json(200, {error: "not found the role"});
        }       
      }
    });
  },


};
