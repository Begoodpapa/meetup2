/*
 unit test cases for Event related functionalities
*/

'use strict';
var supertest = require('supertest');
var eventUtil = require('../lib/eventUtil.js');
var assert = require('assert');

var init_user = function(user_name, id) {
  var user = {};
  user.fullname = user_name;
  user.email = 'gang-layner.wang@nokia.com';
  user.id = id;
  return user;
};

describe('event and eventUtil', function() {

  describe('event relevant functions', function() {

    var eventID;
    var eventOwner;

    before(function(done) {
      User.destroy()
        .then(function(result) {
          return Group.destroy();
        })
        .then(function(result) {
          return Event.destroy();
        })
        .then(function(result) {
          var user = init_user('WangGang', '10239936');
          return User.create(user);
        })
        .then(function(createdUser) {
          var groupObj = {};
          groupObj.name = 'test group';
          groupObj.desc = 'hello world';
          groupObj.owner = createdUser;
          eventOwner = createdUser;
          return Group.create(groupObj);
        })
        .then(function(createdGroup) {
          var eventObj = {};
          eventObj.owner = eventOwner;
          eventObj.desc = 'for test';
          eventObj.group = createdGroup;
          return Event.create(eventObj);
        })
        .then(function(createdEvent) {
          eventID = createdEvent.id;
          done();
        })

    });

    it('add one user to event, test interface', function(done) {

      var user = init_user('Xi JinPing', '00000001');
      User.create(user)
        .then(function(createdUser) {
          eventUtil.addOneUserToEvent(user, eventID, function(err, updatedEvent) {
            if(err) {
              done(err);
            } else {
              assert.equal(updatedEvent.user.length, 1);
              for(var i = 0; i < updatedEvent.user.length; i++) {
                if(updatedEvent.user[i].id === user.id) {
                  done();
                  break;
                }
              }
              if(i === updatedEvent.user.length) {
                throw('add user to event failed');
              }
            }
          })
        })
        .catch(function(err) {
          done(err);
        });

    });

  });

  describe('add one user to group', function() {

    var createdGroupId;

    before(function(done) {

      User.destroy()
        .then(function(result) {
          return Group.destroy();
        })
        .then(function(result) {
          var user = init_user('WangGang', '10239936');
          return User.create(user);
        })
        .then(function(createdUser) {
          var groupObj = {};
          groupObj.name = 'test group';
          groupObj.desc = 'hello world';
          groupObj.owner = createdUser;
          return Group.create(groupObj);
        })
        .then(function(createdGroup) {
          createdGroupId = createdGroup.id;
          done();
        });
    });

    it('add one user to group', function(done) {

      var user = init_user('Xi JinPing', '00000001');
      User.create(user)
        .then(function(createdUser) {
          eventUtil.addUserToGroup(createdGroupId, user, function(err, newGroup) {
            if(err) { return done(err); }
            assert.equal(newGroup.user[0].id, user.id);
            done();
          })
        });
    });

  });

  describe('get mail list of event users and send notify mail', function() {
    var eventID;

    beforeEach(function(done) {

      var user1 = init_user('wanggang', '10239936');
      var user2 = init_user('xi jinping', '00000001');
      var createdEvent;
      var createdUser1;
      var createdUser2;

      Event.destroy()
        .then(function(results) {
          return Mail.destroy();
        })
        .then(function(results) {
          return User.destroy();
        })
        .then(function(results) {
          var event_obj = {};
          event_obj.topic = 'NOKIA 50th birthday Celebration';
          event_obj.desc = 'Hello NOKIA';
          event_obj.address = '19th floor';
          var date = new Date();
          event_obj.begindate = date;
          date = new Date(date.getTime() + 1000);
          event_obj.enddate = date;
          return Event.create(event_obj);
        })
        .then(function(created) {
          createdEvent = created;
          eventID = created.id;
          return User.create(user1)
        })
        .then(function(createdUser) {
          createdUser1 = createdUser;
          return User.create(user2);
        })
        .then(function(createdUser) {
          createdUser2 = createdUser;
          createdEvent.user.add(createdUser1);
          return createdEvent.save();
        })
        .then(function() {
          createdEvent.user.add(createdUser2);
          return createdEvent.save();
        })
        .then(function(createdUser2) {
          done();
        })
        .catch(done);
    });

    it('get the mail list of one event', function(done) {

      eventUtil.getEventUsersMail(eventID, function(err, mail_addrs) {
        if(err) {
          done(err);
        } else {
          assert.equal(mail_addrs[0], 'gang-layner.wang@nokia.com');
          assert.equal(mail_addrs[1], 'gang-layner.wang@nokia.com');
          done();
        }
      });
    });
  });
})