'use strict';
var privilegeUtil = require('../../lib/privilegeUtil.js');
var groupUtil = require('../../lib/groupUtil.js');
var eventUtil = require('../../lib/eventUtil.js');
var Action_Mapping_List = {
  /*event*/
  'eventDoEdit':         { scope: 'event',  isdefault:'no',   right: 'editevent'      },
  'publish':             { scope: 'event',  isdefault:'no',   right: 'publishevent'   },
  'addEventMemberAjax':  { scope: 'event',  isdefault:'yes',  right: 'addeventmember' },
  'InviteFriendAjax':    { scope: 'event',  isdefault:'yes',  right: 'addeventmember' },
  /*group*/
  'addMemberAjax':       { scope: 'group',  isdefault:'yes',  right: 'addgroupmember'},
  'importMemberCSV':     { scope: 'group',  isdefault:'yes',  right: 'addgroupmember'},
  'destroyfile':         { scope: 'group',  isdefault:'no',   right: 'deletefile'    },
  'uploadpaper':         { scope: 'group',  isdefault:'no',   right: 'uploadpaper'   },
  'destroypaper':        { scope: 'group',  isdefault:'no',   right: 'deletepaper'   },
  'destroytest':         { scope: 'group',  isdefault:'no',   right: 'deletetest'    },
  'showdetailreport':    { scope: 'group',  isdefault:'no',   right: 'gettestreport' },
  'getdetailreport':     { scope: 'group',  isdefault:'no',   right: 'gettestreport' },
  /*global*/
  'showAdminDashboard':            { scope: 'global', isdefault:'no', right: 'admincontrol'  },
  'showAdminGlobalPrivilege':      { scope: 'global', isdefault:'no', right: 'admincontrol'  },
  'showAdminGroupPrivilege':       { scope: 'global', isdefault:'no', right: 'admincontrol'  },
  'showAdminSingleGroupPrivilege': { scope: 'global', isdefault:'no', right: 'admincontrol'  },
  'showAdminEventPrivilege':       { scope: 'global', isdefault:'no', right: 'admincontrol'  },
  'showAdminSingleEventPrivilege': { scope: 'global', isdefault:'no', right: 'admincontrol'  },
  'showAdminRoleManage':           { scope: 'global', isdefault:'no', right: 'admincontrol'  },
  'addOrUpdateAdminRole':          { scope: 'global', isdefault:'no', right: 'admincontrol'  },
  'deleteAdminRole':               { scope: 'global', isdefault:'no', right: 'admincontrol'  },
  'updateGlobalPrivilege':         { scope: 'global', isdefault:'no', right: 'admincontrol'  },
  'updateGroupPrivilege':          { scope: 'global', isdefault:'no', right: 'admincontrol'  },
  'updateEventPrivilege':          { scope: 'global', isdefault:'no', right: 'admincontrol'  }
};


module.exports = function(req, res, next) {

  var user = req.session.user;
  var validurl = req.url.split('?')[0];
  var parameters = validurl.split('/');
  var groupid = req.param('gid');
  var eventid = req.param('eid');
  var action = parameters[parameters.length-1];
  var privilegeAction = Action_Mapping_List[action];

  var roleCheck = function(action, role, cb){
    Role.find({name: role,}, function(err, found){
      if(found[0]){
        if(found[0][action]==='yes'){
          return cb(null, 'pass');
        }else{
          return cb(null, 'reject');
        }
      }else{
        return cb(null, 'reject');
      }
    });
  };

  var privilegeCheck = function(action, scope, targetid, cb){
    //console.log('privilegeCheck', user._id, scope, targetid)
    privilegeUtil.getPrivilege(user._id, scope, targetid, function(err, found){
      if(found[0]){
        if(action){
          roleCheck(action.right, found[0].role, function(err, checked){
            return cb(null, checked);
          });
        }else{
          return cb(null, 'reject');
        }
      }else{
        return cb(null, 'reject');
      }
    });
  };  

  var defaultActionCheck = function(action, userid, scope, targetid, cb){
    if(action.isdefault==='yes'){
      if(scope === 'group'){
        groupUtil.findUserFromTheGroup(userid, targetid)
        .then(()=>{
          cb(null, 'pass')
        })
        .catch(()=>{
          cb(null, 'reject')

        })
      }else if((scope === 'event')){
        eventUtil.findUserFromTheEvent(userid, targetid, function(err,user){
          if(!err){
            if(user!==null){
              return cb(null, 'pass');
            }else{
              return cb(null, 'reject');
            }
          }else{
            return cb(null, 'reject');
          }
        });
      }else{
        return cb(null, 'pass');
      }
    }else{
      return cb(null, 'reject');
    }
  }

  var response_fail = function(error_info){
    if(!!req.accepted.length && req.accepted[0].value==='application/json'){
      return res.json(200, {error: error_info});
    }else{
      return res.negotiate(error_info);
    }
  };

  var eventPrivilegeCheck = function(action, cb){

    async.waterfall([

      function(callback){
        privilegeCheck(action, 'event', eventid, callback);
      },

      function(checked, callback){
        if(checked==='pass'){
          cb(null, checked);
        }else{
          defaultActionCheck(action, user._id, 'event', eventid, callback);
        }
      },

      function(checked, callback){
        if(checked==='pass'){
          cb(null, checked);
        }else{
          privilegeCheck(action, 'group', groupid, callback);
        }
      },

      function(checked, callback){
        if(checked==='pass'){
          cb(null, checked);
        }else{
          privilegeCheck(action, 'global', null, callback);
        }
      },

    ], function(err, checked){
      if(err){
        return cb(err, "reject");
      }else{
        return cb(err, checked);
      }
    });
  };

  var groupPrivilegeCheck = function(action, cb){

    async.waterfall([

      function(callback){
        privilegeCheck(action, 'group', groupid, callback);
      },

      function(checked, callback){
        if(checked==='pass'){
          cb(null, checked);
        }else{
          defaultActionCheck(action, user._id, 'group', groupid, callback);
        }
      },

      function(checked, callback){
        if(checked==='pass'){
          cb(null, checked);
        }else{
          privilegeCheck(action, 'global', null, callback);
        }
      },

    ], function(err, checked){
      if(err){
        return cb(err, "reject");
      }else{
        return cb(err, checked);
      }
    });
  };  


  var globalPrivilegeCheck = function(action, cb){

    async.waterfall([

      function(callback){
        privilegeCheck(action, 'global', null, callback);
      },

      function(checked, callback){
        if(checked==='pass'){
          cb(null, checked);
        }else{
          defaultActionCheck(action, user._id, 'global', null, callback);
        }
      },

    ], function(err, checked){
      if(err){
        return cb(err, "reject");
      }else{
        return cb(err, checked);
      }
    });
  };    

  if(privilegeAction){
    //console.log('privilegeAction', privilegeAction.scope)
    if(privilegeAction.scope==='event'){
      eventPrivilegeCheck(privilegeAction, function(err, checked){
        if(checked==='pass'){
          return next();
        } else {
          response_fail('You have no privilege to execute this action');
        }
      });
    } else if(privilegeAction.scope==='group'){
      groupPrivilegeCheck(privilegeAction, function(err, checked){
        if(checked==='pass'){
          return next();
        } else {
          response_fail('You have no privilege to execute this action');
        }
      });
    } else if(privilegeAction.scope==='global'){
      globalPrivilegeCheck(privilegeAction, function(err, checked){
        if(checked==='pass'){
          return next();
        } else {
          response_fail('You have no privilege to execute this action');
        }
      });
    } else {
      response_fail('Unknow privilegeAction scope, url:'+req.url);
    }
  }else{
      response_fail('Unknow privilegeAction, url:' + req.url + ', action:' + action);
  }

};
