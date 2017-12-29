/*
 unit test cases for Group related functionalities
*/

'use strict';
var supertest = require('supertest');
var groupUtil = require('../lib/groupUtil');
var assert = require('assert');

var init_user = function(user_name, userid){
  var user = {};
  user.fullname = user_name;
  user.email = 'gang-layner.wang@nokia.com';
  user.id = userid;
  return user;
};

describe('Group', function() {

  describe('Group creation', function(){
    it('should be created successfully and redirect to new page', function(done) {

      supertest(sails.hooks.http.app)
        .post('/newGroup')
        .send({
          Name: 'groupTest',
          Desc: 'This is one group for test',
          Pic: 123456
        })
        .expect(200)
        .end(function(err, res) {
          if (err) {
            console.log(res.text);
            return done(err);
          }
          done();
        });
    });

    it('should be created failed and response error message', function(done) {

      supertest(sails.hooks.http.app)
        .post('/newGroup')
        .send({
          Name: '',
          Desc: 'This is one group for test'
        })
        .expect(500)
        .expect('{\n  "error": "group name or group description is null"\n}')
        .end(function(err, res) {
          if (err) {
            console.log(res.text);
            return done(err);
          }
          done();
        });
    });

  });

  describe('Get the group user mail list', function(){

    var groupid;

    beforeEach(function(done){
      
      var user1 = init_user('wanggang', '10239936');
      var user2 = init_user('xi jinping', '00000001');
      var createdGroup;
      var createdUser1;
      var createdUser2;

      Group.destroy()
      .then(function(results){
        return User.destroy();
      })
      .then(function(results){
        var group_obj = {};
        group_obj.name ='test group';
        group_obj.desc='hello world';
        group_obj.owner=1;
        group_obj.groupfd='/1.jpg';
        group_obj.tags='innovation';
        return Group.create(group_obj);    
      })
      .then(function(created){
        createdGroup = created;
        groupid = created.id;
        return User.create(user1)
      })
      .then(function(createdUser){
        createdUser1 = createdUser;
        return User.create(user2);
      })
      .then(function(createdUser){
        createdUser2 = createdUser;
        createdGroup.user.add(createdUser1);
        return createdGroup.save();
      })
      .then(function(){
        createdGroup.user.add(createdUser2);
        return createdGroup.save();
      })
      .then(function(createdUser2){
        done();
      })
      .catch(done);
    });

    it('get the mail list of one group', function(done){
      
      groupUtil.getGroupUsersMail(groupid, function(err, mail_addrs){
        if(err){
          done(err);
        }else{
          assert.equal(mail_addrs.length, 2);
          assert.equal(mail_addrs[0], 'gang-layner.wang@nokia.com');
          assert.equal(mail_addrs[1], 'gang-layner.wang@nokia.com');
          done();
        }
        
      });
    });

    it('send notify mail to group users', function(done){

        MailService.startMailService();
        Mail.destroy()
        .then(function(saved){
            var mail_obj ={};
            mail_obj.subject ='hello world for group users';
            mail_obj.content ='from layner';
            mail_obj.date=new Date();
            console.log(groupid);
            groupUtil.sendNotifyMailToGroupUsers(groupid, mail_obj, function(err){
              setTimeout(function(){  
                Mail.find({state:'done'})
                .then(function(result){
                    assert.equal(result.length, 1);
                    done();
                })
                .catch(done);
              }, 30000);
            });
        })
        .catch(done);
    });
  });
});