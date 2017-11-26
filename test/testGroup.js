'use strict';

var supertest = require('supertest');
var groupUtil = require('../lib/groupUtil');
var assert = require('assert');

const { auth, init_user, createUser, createGroup, createEvent, createCommingEvent, createPassedEvent} = require('./utils/common')

const BASE_URL = '/'
const URLS = {
  GROUP_GET: BASE_URL + 'group/getGroupsAjax',
  GROUP_CREATE: BASE_URL + 'group/createAjax',
  GROUP_LOAD_ONE: BASE_URL + 'group/1/loadoneGroupAjax',
  GROUP_UPDATE: BASE_URL + 'group/updateAjax',
  GROUP_DELETE: BASE_URL + 'group/deleteAjax',
  SHOW_MY_GROUP: BASE_URL + 'user/showMyGroupAjax',
  SHOW_MY_PROFILE: BASE_URL + 'user/showProfileAjax',
}
const userName = 'yaolin'
const userId = '61467748'
const groupName= 'group1'
const eventName= 'event1'
const user = init_user(userName, userId)

describe('Group', function() {

  var agent;

  before(function(done) {
    agent = supertest.agent(sails.hooks.http.app)

    Promise.resolve()
    .then(User.destroy)
    .then(Group.destroy)
    .then(User.create.bind(null, user))
    .then(auth.bind(null, agent, user))
    .then(done)
  });


	describe('GroupController.createAjax', function(){
    after(done=>{
      Group.destroy()
      .then(()=>done())
    })

		it('should be created successfully and redirect to new page', function(done) {
      agent
				.post(URLS.GROUP_CREATE)
				.send({
					Name: 'groupTest',
					Desc: 'This is one group for test',
					Pic: 123456
				})
				.expect(200)
				.end(function(err, res) {
					if (err) {
						//console.log(res.text);
						return done(err);
					}
					done();
				});
		});

		it('should be created failed and response error message', function(done) {

			agent
				.post(URLS.GROUP_CREATE)
				.send({
					Name: 'groupTest',
					Desc: 'This is one group for test'
				})
				.expect(400)
				.end(function(err, res) {
					done();
				});
		});
	});

	describe('GroupController.getGroupsAjax', function(){
		it('should be correct get groups info', function(done) {

      agent
				.post(URLS.GROUP_GET)
				.send()
				.expect(200)
				.end(function(err, res) {
					if (err) {
						return done(err);
					}
					done();
				});
		});
	});


	describe('loadoneGroupAjax', function(){

    before(done=>{
      Promise.resolve()
      .then(_=> createUser('yaolin', '61467748'))
      .then(_=> createUser('yaolin2', '61467749'))
      .then(_=> User.findOne({uid: userName}))
      .then(user => createGroup({name: groupName}, user))
      .then(group=>{
        return Promise.all([createPassedEvent(group), createCommingEvent(group)])
      })
      .then(()=>done())
      .catch(done)
    })

    it('loadoneGroupAjax should be correct', (done)=>{

      agent
				.get(URLS.GROUP_LOAD_ONE)
				.expect(200)
				.end(function(err, res) {
          //console.log(res.body)
          const {comingEvents, RecentEvent, pastEvents, events, group, user, ingroup} = res.body
          assert.equal(comingEvents.length, 1)
          assert.equal(pastEvents.length, 1)
          assert.equal(events.length, 2)
          assert.equal(group.name, groupName)
          assert.equal(user.uid, userName)
          assert.equal(ingroup, true)
          assert.equal(group.user.length, 3)
          assert.equal(group.user[0].fullname, userName)

					if (err) {
						return done(err);
					}
					done();
				});
    })
  })

	describe('UserController.showMyGroupAjax', function(){
    before(done=>{
      Promise.resolve()
      .then(_=> createUser('yaolin', '61467748'))
      .then(_=> createUser('yaolin2', '61467749'))
      .then(_=> User.findOne({uid: userName}))
      .then(user => createGroup({name: groupName, userIds: [user._id]}, user))
      .then(group=>{
        return Promise.all([createPassedEvent(group), createCommingEvent(group)])
      })
      .then(()=>done())
      .catch(done)
    })

    it('loadoneGroupAjax should be correct', (done)=>{

      agent
				.get(URLS.SHOW_MY_GROUP)
				.expect(200)
				.end(function(err, res) {
          //console.log(res.body)
          const {groups} = res.body

          assert.equal(groups.length, 1);

					if (err) {
						done(err);
					}
					done();
				});
    })
  })

	describe('UserController.profile', function(){
    before(done=>{
      Promise.resolve()
      .then(_=> createUser('yaolin', '61467748'))
      .then(_=> createUser('yaolin2', '61467749'))
      .then(_=> User.findOne({uid: userName}))
      .then(user => createGroup({name: groupName, userIds: [user._id]}, user))
      .then(group=>{
        return Promise.all([createPassedEvent(group), createCommingEvent(group)])
      })
      .then(()=>done())
      .catch(done)
    })

    xit('show profile should be correct', (done)=>{

      agent
				.get(URLS.SHOW_MY_PROFILE)
				.expect(200)
				.end(function(err, res) {
          //console.log(res.body)

					if (err) {
						done(err);
					} else{
            done();
          }
				});
    })
  })


});
