const { getCommingEventByGroupid, getPassedEventByGroupid } = require('../../lib/eventUtil')
const { assert } = require('chai')
const {init_user, createUser, createGroup, createEvent, createCommingEvent, createPassedEvent} = require('./common')


describe('EventUtil', ()=>{
  before(done=>{
    userName = 'yaolin'
    groupName= 'group1'
    eventName= 'event1'

    Promise.resolve()
    .then(_=> createUser('yaolin', '61467748'))
    .then(_=> createUser('yaolin2', '61467749'))
    .then(_=> User.findOne({uid: userName}))
    .then(user => createGroup({name: groupName}, user))
    .then(()=>done())
    .catch(done)
  })

  describe('getCommingEventByGroupid', ()=>{
    beforeEach(done=>{
      Event.destroy()
      .then(()=>done())
    })
  
    it('getCommingEventByGroupid can get comming event', (done)=>{
      Group.findOne({name: groupName})
      .then(createCommingEvent)
      .then(getCommingEventByGroupid.bind(null, 1))
      .then(events=>{
        assert.equal(events.length, 1);
        done()
      })
    })

    it('getCommingEventByGroupid cant get passed event', (done)=>{
      Group.findOne({name: groupName})
      .then(createPassedEvent)
      .then(getCommingEventByGroupid.bind(null, 1))
      .then(events=>{
        assert.equal(events.length, 0);
        done()
      })
    })
  })

  describe('getPassedEventByGroupid', ()=>{
    beforeEach(done=>{
      Event.destroy()
      .then(()=>done())
    })
  
    it('getPassedEventByGroupid can get comming event', (done)=>{
      Group.findOne({name: groupName})
      .then(createCommingEvent)
      .then(getPassedEventByGroupid.bind(null, 1))
      .then(events=>{
        assert.equal(events.length, 0);
        done()
      })
    })

    it('getCommingEventByGroupid cant get passed event', (done)=>{
      Group.findOne({name: groupName})
      .then(createPassedEvent)
      .then(getPassedEventByGroupid.bind(null, 1))
      .then(events=>{
        assert.equal(events.length, 1);
        done()
      })
    })
  })

})
