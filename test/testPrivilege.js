'use strict';

var privilegeUtil = require('../lib/privilegeUtil.js');
var assert = require('assert');

var init_user = function(user_name, id){
    var user = {};
    user.fullname = user_name;
    user.email = 'gang-layner.wang@nokia.com';
    user.id = id;
    return user;
};


describe.only('test privilege', function(){

  beforeEach(function(done){

    User.destroy()
    .then(function(result){
      return Privilege.destroy();
    })
    .then(function(result){
      var user = init_user('WangGang','10239936');
      return User.create(user);
    })
    .then(function(createdUser){
      var privilegeObj = {};
      privilegeObj.userid = '00000001';
      privilegeObj.groupid = null;
      privilegeObj.scope = 'global';
      privilegeObj.role = 'administrator';
      return Privilege.create(privilegeObj);
    })
    .then(function(createdPrivilege){
      var privilegeObj = {};
      privilegeObj.userid = '00000002';
      privilegeObj.groupid = null;
      privilegeObj.scope = 'global';
      privilegeObj.role = 'actingadministrator';
      return Privilege.create(privilegeObj);
    })
    .then(function(createdPrivilege){
      var privilegeObj = {};
      privilegeObj.userid = '00000003';
      privilegeObj.groupid = null;
      privilegeObj.scope = 'global';
      privilegeObj.role = 'globalspecial';
      return Privilege.create(privilegeObj);
    })
    .then(function(createdPrivilege){
      var privilegeObj = {};
      privilegeObj.userid = '00000004';
      privilegeObj.groupid = null;
      privilegeObj.scope = 'global';
      privilegeObj.role = 'globaluser';
      return Privilege.create(privilegeObj);
    })
    .then(function(createdPrivilege){
      var privilegeObj = {};
      privilegeObj.userid = '00000011';
      privilegeObj.groupid = null;
      privilegeObj.scope = 'group';
      return Privilege.create(privilegeObj);
    })
    .then(function(createdPrivilege){
      var privilegeObj = {};
      privilegeObj.userid = '00000012';
      privilegeObj.groupid = null;
      privilegeObj.scope = 'group';
      return Privilege.create(privilegeObj);
    })
    .then(function(createdPrivilege){
      var privilegeObj = {};
      privilegeObj.userid = '00000013';
      privilegeObj.groupid = null;
      privilegeObj.scope = 'group';
      return Privilege.create(privilegeObj);
    })
    .then(function(createdPrivilege){
      var privilegeObj = {};
      privilegeObj.userid = '00000014';
      privilegeObj.groupid = null;
      privilegeObj.scope = 'group';
      return Privilege.create(privilegeObj);
    })
    .then(function(createdPrivilege){
      return done();
    })
    .catch(function(err){
      console.log(err);
      return done(err);
    });

  });

  describe.only('global privilege configuration', function(){

    it('set one user as administrator', function(done){

      var userid = '10239936';

      privilegeUtil.assignUserPrivilege(userid, 'administrator', null, function(err, userPrivilege){
        if(err) {return done(err);}
        assert.equal(userPrivilege.userid, userid);
        assert.equal(userPrivilege.role, 'administrator');
        assert.equal(userPrivilege.scope, 'global');
        assert.equal(userPrivilege.deletegroup,'yes');
        done();
      });

    });

    it('set one user as acting administrator in global', function(done){

      var userid = '10239936';

      privilegeUtil.assignUserPrivilege(userid, 'actingadministrator', null, function(err, userPrivilege){
        if(err) {return done(err);}
        assert.equal(userPrivilege.userid, userid);
        assert.equal(userPrivilege.role, 'actingadministrator');
        assert.equal(userPrivilege.scope, 'global');
        done();
      });

    });

    it('set one user as special in global', function(done){

      var userid = '10239936';

      privilegeUtil.assignUserPrivilege(userid, 'globalspecial', null, function(err, userPrivilege){
        if(err) {return done(err);}
        assert.equal(userPrivilege.userid, userid);
        assert.equal(userPrivilege.role, 'globalspecial');
        assert.equal(userPrivilege.scope, 'global');
        done();
      });

    });

  });

  describe('group privilege configuration', function(){

    it('set one user as group owner', function(done){

      var userid = '10239936';
      var groupid = 1;

      privilegeUtil.assignUserPrivilege(userid, 'groupowner', groupid, function(err, userPrivilege){
        if(err) {return done(err);}
        assert.equal(userPrivilege.userid, userid);
        assert.equal(userPrivilege.role, 'groupowner');
        assert.equal(userPrivilege.scope, 'group');
        done();
      });

    });

    it('set one user as top user in group', function(done){

      var userid = '10239936';
      var groupid = 1;

      privilegeUtil.assignUserPrivilege(userid, 'groupactingowner', groupid, function(err, userPrivilege){
        if(err){return done(err);}
        assert.equal(userPrivilege.userid, userid);
        assert.equal(userPrivilege.role, 'groupactingowner');
        assert.equal(userPrivilege.scope, 'group');
        done();
      });

    });

    it('set one user as special user in group', function(done){

      var userid = '10239936';
      var groupid = 1;

      privilegeUtil.assignUserPrivilege(userid, 'groupspecial', groupid, function(err, userPrivilege){
        if(err){return done(err);}
        assert.equal(userPrivilege.userid, userid);
        assert.equal(userPrivilege.role, 'groupspecial');
        assert.equal(userPrivilege.scope, 'group');
        done();
      });

    });

  });

  describe('one user has multiple roles', function(){

    it('one user has multiple role in one group', function(done){

      var userid = '10239936';
      var groupid = 1;

      privilegeUtil.assignUserPrivilege(userid, 'groupowner', groupid, function(err, userPrivilege){
        privilegeUtil.assignUserPrivilege(userid, 'groupspecial', groupid, function(err, userPrivilege){
          assert.equal(err, 'user has been assigned relevant privilege in group');
          assert.equal(userPrivilege, null);
          done();
        });
      });
    });

    it('one user has multiple role in global', function(done){

      var userid = '10239936';

      privilegeUtil.assignUserPrivilege(userid, 'administrator', null, function(err, userPrivilege){
        privilegeUtil.assignUserPrivilege(userid, 'actingadministrator', null, function(err, userPrivilege){
          assert.equal(err, 'user has been assigned relevant privilege in global');
          assert.equal(userPrivilege, null);
          done();
        });
      });
    });

    it('one user has one role in global and one role in group', function(done){

      var userid = '10239936';
      var groupid = 1;

      privilegeUtil.assignUserPrivilege(userid, 'administrator', null, function(err, userPrivilege){
        privilegeUtil.assignUserPrivilege(userid, 'groupowner', groupid, function(err, userPrivilege){
          assert.equal(err, null);
          assert.equal(userPrivilege.role, 'groupowner');
          done();
        });
      });
    });

  });

  describe('get the privilege of one user', function(){

    it('get the global privilege of one user', function(done){

      var userid = '10239936';

      privilegeUtil.assignUserPrivilege(userid, 'administrator', null, function(err, assignedPrivilege){

        if(err){return done(err);}

        privilegeUtil.getUserGlobalPrivilege(userid, function(err, userPrivilege){
          assert.equal(userPrivilege[0].userid, userid);
          assert.equal(userPrivilege[0].groupid, null);
          assert.equal(userPrivilege[0].role, 'administrator');
          assert.equal(userPrivilege[0].scope, 'global');
          done();
        });

      }); 
    });

    it('get the group privilege of one user', function(done){

      var userid = '10239936';
      var groupid = '1';

      privilegeUtil.assignUserPrivilege(userid, 'groupowner', groupid,  function(err, assignedPrivilege){

        if(err){return done(err);}
        
        privilegeUtil.getUserGroupPrivilege(userid, groupid, function(err, userPrivilege){
          assert.equal(userPrivilege[0].userid, userid);
          assert.equal(userPrivilege[0].groupid, groupid);
          assert.equal(userPrivilege[0].role, 'groupowner');
          assert.equal(userPrivilege[0].scope, 'group');
          done();
        });

      }); 
    });

  });

  describe('init privilege database', function(){
    it('init global privilege', function(done){

      privilegeUtil.initPrivileges(function(err){
        if(err) {done(err);}

        Privilege.find({scope: 'global'}, function(err, founds){
          assert.equal(founds.length>=4, true);
          done();
        })

      });


    });

    it('init group privilege', function(done){

      privilegeUtil.initPrivileges(function(err){
        if(err) {done(err);}

        Privilege.find({scope: 'group'}, function(err, founds){
          assert.equal(founds.length>=4, true);
          done();
        })
      });

    });
  });

  describe('update user privilege', function(){
    
    it('update user global privilge', function(done){
      
      var userid = '10239937';

      privilegeUtil.assignUserPrivilege(userid, 'administrator', null, function(err, assignedPrivilege){

        if(err){return done(err);}

        privilegeUtil.updateUserGlobalPrivilege(userid, {deletegroupmember:'no'}, function(err, updatedPrivilege){
          if(err){done(err);}
          assert.equal(updatedPrivilege.userid, userid);
          assert.equal(updatedPrivilege.groupid, null);
          assert.equal(updatedPrivilege.role, 'administrator');
          assert.equal(updatedPrivilege.scope, 'global');
          assert.equal(updatedPrivilege.deletegroupmember, 'no');
          done();
        });

      });
    });

    it('update user group privilege', function(done){

      var userid = '10239936';
      var groupid = '1';

      privilegeUtil.assignUserPrivilege(userid, 'groupowner', groupid,  function(err, assignedPrivilege){

        if(err){return done(err);}
        
        privilegeUtil.updateUserGroupPrivilege(userid, groupid, {deleteevent:'no'}, function(err, updatedPrivilege){
          if(err){done(err);}
          assert.equal(updatedPrivilege.userid, userid);
          assert.equal(updatedPrivilege.groupid, groupid);
          assert.equal(updatedPrivilege.role, 'groupowner');
          assert.equal(updatedPrivilege.deleteevent, 'no');
          done();
        });

      });

    });

  });

  
});