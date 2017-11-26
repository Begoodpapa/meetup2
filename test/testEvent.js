'use strict';
var supertest = require('supertest');
var assert = require('assert');
var Promise = require('bluebird');

const {
  auth,
  init_user, 
  createUser, 
  createGroup,
  createEvent,
  createCommingEvent,
  createPassedEvent} = require('./utils/common')

const BASE_URL = '/'
const URLS = {
  EVENT_DO_CREATE: groupId =>`${BASE_URL}group/${groupId}/newEvent`,
  EVENT_DO_EDIT: (groupid, eventid)=>`${BASE_URL}group/${groupid}/event/${eventid}/eventDoEdit`,
  EVENT_INVITE_FRIEND: eventid=>`${BASE_URL}event/${eventid}/InviteFriendAjax`,
  EVENT_ADD_MEMBER: eventid=>`${BASE_URL}event/${eventid}/addEventMemberAjax`, //addUsersToEvent
  EVENT_PUBLISH: (groupid, eventid) => `${BASE_URL}group/{groupid}/event/${eventid}/publish`,
  EVENT_SHOW_AJAX: (groupId, eventId) =>`${BASE_URL}group/${groupId}/event/${eventId}/show`,
  EVENT_SHOW_MY_EVENT: BASE_URL + 'user/showMyEventAjax',
  GROUP_LOAD_ONE: BASE_URL + 'group/1/loadoneGroupAjax',
  GROUP_UPDATE: BASE_URL + 'group/updateAjax',
  GROUP_DELETE: BASE_URL + 'group/deleteAjax',
}
const userName = 'yaolin'
const userId = '61467748'
const groupName= 'group1'
const eventName= 'event1'
const user = init_user(userName, userId)

function createEventAjax(agent, groupid, topic, publish=false){
  return new Promise((resolve, reject)=>{
    agent
    .post(URLS.EVENT_DO_CREATE(groupid))
    .send({
      Topic: topic,
      Group: groupid,
      Address: '3',
      beginDate: '2017-11-14',
      BeginTime: '23:30',
      endDate: '2017-11-16',
      EndTime: '10:30',
      EventDetail: 'detail',
      Tag:[],
      Publish: publish,
    })
    .expect(200)
    .end((err, res)=>{
      err? reject(err): resolve(res)
    })
  })
}

function editEventAjax(agent, groupid, eventid, topic, publish=false){
  return new Promise((resolve, reject)=>{
    agent
    .post(URLS.EVENT_DO_EDIT(groupid, eventid))
    .send({
      Topic: topic,
      Group: groupid,
      Address: '3',
      beginDate: '2017-11-14',
      BeginTime: '23:30',
      endDate: '2017-11-16',
      EndTime: '10:30',
      EventDetail: 'detail',
      Tag:[],
      Publish: publish,
    })
    .expect(200)
    .end((err, res)=>{
      err? reject(err): resolve(res)
    })
  })
}

function inviteFriendAjax(agent, eventid, from, email){
  return new Promise((resolve, reject)=>{
    agent
    .post(URLS.EVENT_INVITE_FRIEND(eventid))
    .send({
      from: from,
      email: email,
      eid: eventid, //event id is mandantory for privilege check???
    })
    .expect(200)
    .end((err, res)=>{
      err? reject(err): resolve(res)
    })
  })
}

function eventAddMemberAjax(agent, eventid, users){
  return new Promise((resolve, reject)=>{
    agent
    .post(URLS.EVENT_ADD_MEMBER(eventid))
    .send({
      users: users,
      eid: eventid,
    })
    .expect(200)
    .end((err, res)=>{
      err? reject(err): resolve(res)
    })
  })
}

function eventPublish( agent, groupid, eventid ){
  return new Promise((resolve, reject)=>{
    agent
    .post(URLS.EVENT_PUBLISH(groupid, eventid))
    .send({
      gid: groupid,
      eid: eventid,
    })
    .expect(302)
    .end((err, res)=>{
      err? reject(err): resolve(res)
    })
  })
}

function eventShowMyEvent( agent ){
  return new Promise((resolve, reject)=>{
    agent
    .post(URLS.EVENT_SHOW_MY_EVENT)
    .send()
    .expect(200)
    .end((err, res)=>{
      err? reject(err): resolve(res)
    })
  })
}

describe('Event', function() {

  var agent;
  var createdGroup
  var createdUser
  var createdEvent

  before(function(done) {
    agent = supertest.agent(sails.hooks.http.app)

    Promise.resolve()
    .then(User.destroy)
    .then(Group.destroy)
    .then(()=>{
       return Promise.using(User.create(user), createdUser=>{
         return Promise.using(createGroup({name: groupName, userIds: [createdUser._id, '61467749']}, createdUser), createGroup=>{
           return auth(agent, createdUser)
         })
      })
    })
    .then(()=>{
      done()
    })
  });

	describe('EventController.doCreate', function(){


    function createEventInModal(groupId){
      const params = {
        Topic: 'topic',
        group: groupId,
        Address: '3',
        beginDate: '2017-11-14',
        BeginTime: '23:30',
        endDate: '2017-11-16',
        EndTime: '10:30',
        EventDetail: 'detail',
        Tag:[],
        Publish: false
      }
      return Event.create(params)
    }

		it('doCreate should be ok', done => {
      Promise.using(Group.findOne({name: groupName}), findGroup => {
        createEventAjax(agent, findGroup.id, 'topic2')
        .then(res=>{
          assert.equal(res.body.id, findGroup.id);
          done();
        })
        .catch(done)
		});

    it('event showAjax should be ok', done=>{
      Promise.using(Group.findOne({name: groupName}), findGroup => {
        createEventInModal(findGroup.id)
        .then((createdEvent)=>{
          agent
            .get(URLS.EVENT_SHOW_AJAX(findGroup.id, createdEvent.id))
            .send()
            .expect(200)
            .end(function(err, res) {
              //assert.equal(res.body.id, findGroup.id);
              if (err) {
                return done(err);
              }
              done();
            });
          })
        })
      })
    })
  })


	describe('EventController.doEdit', function(){
		it('doEdit should be ok', function(done) {
      Promise.using(Group.findOne({name: groupName}), findGroup=>{
        createEventAjax(agent, findGroup.id, 'topic2')
        .then(result=>{
          const eventid = result.body.id
          return editEventAjax(agent, findGroup.id, eventid, 'topic3')
        })
        .then(()=>{
          done()
        })
      })
		});
  })

	describe('EventController.invitefriends', function(){
		it('invitefriends should be ok', function(done) {
      Promise.using(Group.findOne({name: groupName}), findGroup=>{
        createEventAjax(agent, findGroup.id, 'topic2')
        .then(result=>{
          const eventid = result.body.id
          return inviteFriendAjax(agent, eventid, userName, 'yao.lin@nokia-sbell.com' )
        })
        .then(()=>{
          done()
        })
      })
		});
  })

	describe('EventController.addEventMemberAjax', function(){
		it('addEventMemberAjax should be ok', function(done) {
      Promise.using(Group.findOne({name: groupName}), findGroup=>{
        createEventAjax(agent, findGroup.id, 'topic2')
        .then(result=>{
          const eventid = result.body.id
          return eventAddMemberAjax(agent, eventid, [userId])
        })
        .then(()=>{
          done()
        })
      })
		});
  })

	describe('EventController.publish', function(){
		it('publish should be ok', function(done) {
      Promise.using(Group.findOne({name: groupName}), findGroup=>{
        createEventAjax(agent, findGroup.id, 'topic2')
        .then(result=>{
          const eventid = result.body.id
          return eventPublish(agent, findGroup.id, eventid)
        })
        .then(()=>{
          done()
        })
      })
		});
  })

	describe('EventController.showMyEventAjax', function(){
		it('showMyEventAjax should be ok', function(done) {
      Promise.using(Group.findOne({name: groupName}), findGroup=>{
        createEventAjax(agent, findGroup.id, 'topic2')
        .then(result=>{
          const eventid = result.body.id
          return eventShowMyEvent(agent)
        })
        .then(()=>{
          done()
        })
      })
		});
  })
})
