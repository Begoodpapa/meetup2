'use strict';
/* global Group,ICSParse*/

var eventUtil = require('../../lib/eventUtil.js');
var personaUtil = require('../../lib/personaUtil.js');
var fileUtil = require('../../lib/fileUtil.js');
var privilegeUtil = require('../../lib/privilegeUtil.js');
var Promise = require('bluebird');

const { addOwnerToEvent, } = require('../../lib/eventUtil')

function populateAllUsers(event){
  return event.populateUser()
  .then(users=>{
    event.user = users
    return Promise.resolve(event)
  })
}

module.exports = {

  create: function(req, res) {

    var groupid = req.param('gid');
    var action = 'create';
    var target = {};
    var attached_tags_list = '[]';

    target.topic = '';
    target.desc = '';
    target.address = '';
    target.begindate = '';
    target.enddate = '';
    

    Group.find({
      id: groupid
    }, function(err, found) {
      if (err) {
        console.log('Something is wrong:', err);
        return res.negotiate(err);
      } else {

        Tag.find({}).exec(function(err, tags){
          if(err){
            sails.log.error(err);
            return res.negotiate(err);
          } else {

            var all_tags_str = JSON.stringify(tags);

            res.view('event/EventManager', {
            title: 'New Event',
            action: action,
            user: req.session.user,
            target: target,
            group: found,
            attached_tags_json: attached_tags_list,
            all_tags_json: all_tags_str,
            layout: null
            });
          }
        });
      }
    });
  },

  edit: function(req, res) {
    var eventid = req.param('eid');
    var groupid = req.param('gid');
    var owngroup, attached_tags_list;
    var action='edit';


    Event.findOne({
      id: eventid
    }).populate('group').exec(function(err, found) {
      if (err) {
        sails.log.error(err);
        return res.negotiate(err);
      } else {

        owngroup = found.group;
        attached_tags_list = ((found.tags===undefined) || (found.tags===null)) ? '[]' : found.tags; 

        var group = [];
        group.push(owngroup);

        Tag.find({}).exec(function(err, tags){
          if(err){
            sails.log.error(err);
            return res.negotiate(err);
          } else {

            var all_tags_str = JSON.stringify(tags);

            res.view('event/EventManager', {
            title: 'Edit Event',
            action: action,
            user: req.session.user,
            target: found,
            group: group,
            attached_tags_json: attached_tags_list,
            all_tags_json: all_tags_str,
            layout: null
            });
          }
        });
      }
    });
  },

  publish:function(req, res){
    var groupid = req.param('gid');
    var eventid = req.param('eid');

    Event.findOne({
      id: eventid
    }).exec(function(err, found) {
      if (err) {

        sails.log.error(err);
        return res.negotiate(err);

      } else {

        Event.update(eventid, {
          publish: true,
        }).exec(function(err, updated) {
          if (err) {
            sails.log.error(err);
            return res.negotiate(err);
          } else {
            if(updated[0].publish == true){
              var cb = function(err, created_mail){
                if(err){ console.log(err); }
              };
              eventUtil.sendNotifyMailOnEventCreate(updated[0], cb);
            }
            return res.redirect('/group/'+groupid+'/event/'+ eventid +'/show');
          }
        });

      }
    });
  },

  editPicDesc: function(req, res){
    var gid = req.param('gid');
    var eventid = req.param('eid');
    var desc = req.param('Desc');

     Event.update({
       id: eventid
     }, {
       phoDescription: desc
     }).exec(function(err, updated) {
       if (err) {
         sails.log.error(err);
         return res.negotiate(err);
       }

       var url = '/group/'.concat('show/', gid).concat('#/group/', gid, '/photos');
       return res.redirect(url);
     });
    
  },

  showAjax: function(req, res) {

    const eventId = req.param('eid');
    const user = req.session.user;
    const userId = user._id

    function checkEventExist(event){
      if (!event){
        throw new Error('no event is found')
      } else {
        return Promise.resolve(event)
      }
    }

    Event.findOne({id: eventId})
    .populate('group')
    .then(checkEventExist)
    .then(populateAllUsers)
    .then(event=>{
      const inGroup = !!~event.group.userIds.indexOf(userId)
      const inEvent = !!~event.userIds.indexOf(userId)
      const attached_tags_list = ((event.tags===undefined) || (event.tags===null)) ? '[]' : event.tags;
      const owner = (!!user) && (event.owner === user.id)

      return res.json(200, 
      	{
	      	event: event, 
	        user: user,
	        inevent: inEvent,
	        group: event.group,
	        ingroup: inGroup,
	        owner: owner,
	        layout: null,
	        attached_tags_json: attached_tags_list
        }
      );
    })
    .catch(res.negotiate)
  },

  doCreate: function(req, res) {
    const assignPrivilegeAsync = Promise.promisify(privilegeUtil.assignPrivilege)

    var newEvent = eventUtil.createEventObjFromHttp(req);
    var user = req.session.user;
    let createdEvent;

    function sentNotiyIfPublish(event){
      if(!!event.publish){
        return eventUtil.sendNotifyMailOnEventCreate(events[0],cb);
      }else{
        return Promise.resolve()
      }
    }

    Event.create(newEvent)
    .then(event=>{
      createdEvent = event
      return addOwnerToEvent(event, user._id)
    })
    .then(()=> sentNotiyIfPublish(createdEvent))
    .then(()=> assignPrivilegeAsync(user._id, 'eventowner', 'event', createdEvent.id))
    .then(()=> res.json(200, {id: createdEvent.id}))
    .catch(res.negotiate)
  },


  doEdit: function(req, res) {
    
    var eventid = req.param('eid');
    var updatedEvent = eventUtil.createEventObjFromHttp(req);
    
    Event.update({
      id: eventid
    }, updatedEvent).exec(function(err, updated) {
      if (err) {
        if(err.code==='E_VALIDATION'){
          var beginDateStr = req.param('beginDate') + ' ' + req.param('BeginTime');
          var endDateStr = req.param('endDate') + ' ' + req.param('EndTime');
          var errMsg = 'Begin Date \"'+beginDateStr+'\" should be before End Date \"'+endDateStr+'\", please check';
          sails.log.error(errMsg);
          // return res.json(JSON.stringify({ error: errMsg}));
          return res.send({ error: errMsg});
        }
        sails.log.error(err);
        return res.negotiate(err);
      }

      if(updated[0].publish == true){
        var cb = function(err, created_mail){
          if(err){ console.log(err); }
        };

        updatedEvent.id = eventid;  // event ID is required as part of a unique mail UID
        eventUtil.sendNotifyMailOnEventCreate(updatedEvent, cb);
      }

      return res.json(200, {id:updated[0].id});
    });

  },


  upload: function(req, res) {
    var icsFile = req.file('ics');

    icsFile.upload({
      dirname: sails.config.upload.calender
    }, function(err, files) {
      if (err) {
        return res.negotiate(err);
      }

      if (files.length === 0) {
        return res.badRequest('No ICS file uploaded');
      }

      var file = files[0].fd;
      ICSParse.icsFiletoEvent(file, function(err, event) {
        if (err) {
          return res.negotiate(err);
        }

        var groupId = req.param('group');

        Event.create({
            topic: event.topic,
            desc: event.desc,
            begindate: event.start,
            enddate: event.end,
            address: event.address,
            calenderFile: file,
            group: {
              id: groupId
            }
          })
          .then(function(obj) {
            res.json(obj);
          }).catch(function(e) {
            res.negotiate(e);
          });

      });
    });

  },

  imageUpload: function(req, res) {

    var eventImg = req.file('imgFile');
    var eventID = req.param('eventID');
    var hash = req.param('hash');
    var targetDir, dirName, saveAs;
    
    if( hash){
      targetDir = '/event_' + hash;  
    }else{
      targetDir = '/event_' + eventID;
    }

    dirName = require('path').join(sails.config.appPath, sails.config.assetsdir.directory, sails.config.upload.eventpic.root, targetDir);
    saveAs = eventImg._files[0].stream.filename;
    fileUtil.fileUpload(eventImg, dirName, saveAs, function(err){
      if (err) {
        return res.json(200, {error: 1, message: err});
      }else{
        var url =  sails.config.upload.eventpic.root + targetDir + '/'+ saveAs;
        return res.json(200, { error: 0, url: url }); 
      }
    });

  },

  addUserToEvent: function(req, res){

    var user = req.session.user;
    var eventid = req.param('id');
    var skill = 1;
    var eventlevel = 1;
    var eventscore = 5;
    
    eventUtil.addOneUserToEvent(user, eventid, function(err, updatedEvent){
      if(err){
        return res.json(500, {'err': err});
      }

      // TODO: is it logical to add user to group? maybe we should merely add user to the event?
      eventUtil.addUserToGroup(updatedEvent.group.id, user, function(err) {
        if(err){ console.log(err);}
      });
      
      // send email meeting request to new joined user
      eventUtil.sendEventMailToUser(updatedEvent, user.email);

      personaUtil.updateScore(user.id, skill, eventid, updatedEvent.topic, eventlevel, eventscore, function(){
        return res.json(200, user);  
      });
      
    });
    
  },

  removeUserFromEvent: function(req, res) {

    var user = req.session.user;
    var eventid = req.param('id');
    Event.find({
      id: eventid
    }).populate('user').exec(function(err, events) {
      if (err) {
        err = 'Failed to query database with eventid: ' + eventid;
        sails.log.error(err);
        return res.negotiate(err);

      } else {
        events[0].user.remove(user.id);
        events[0].save(function(err, s) {
          if (err) {
            sails.log.error(err);
            return res.negotiate(err);
          } else {
            return res.json(200, {id: user.id, fullname: user.fullname});
          }
        });
      }
    });
  },


  addUsersToEvent: function(req, res) {
    var eventid = req.param('id');
    var users = req.param('users');

    async.waterfall([
      function(callback){
        async.map(users, function(user, cb){
          User.findOne({_id: user}, cb);
          }, callback);

      },

      function(users, callback){
        async.map(users, function(user, cb){
          eventUtil.addOneUserToEvent(user, eventid, cb);
          }, callback);
      }

      ],

      function(err, result){
        if(err) {return res.negotiate(err);}
        return res.json(result);
      });
    
  },

  InviteFriendToEvent: function(req, res) {
    var eventid = req.param('id');
    var to = req.param('email');
    var from = req.param('from');

    Event.find({
      id: eventid
    }).exec(function(err, events){
      if (err) {
        sails.log.error(err);
        return res.negotiate(err);
      }

      if (events.length === 0) {
        err = 'No event is found with event id:' + eventid;
        sails.log.error(err);
        return res.negotiate(err);
      }

      //console.log("InviteFriendToEvent: from " + from + ", to " + to);
      var subject = "Your friend " + from + " invite you to Beehive event: " + events[0].topic;
      eventUtil.sendEventMailToUser(events[0], to, subject); 
      
      return res.json(200);
    });
    
  },

};
