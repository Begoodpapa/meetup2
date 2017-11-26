'user strict';

// For iCalendar Transport-Independent Interoperability Protocol (iTIP)
// Refer to: https://www.rfc-editor.org/rfc/rfc5546.txt
var ical = require('ical-generator');
var moment = require('moment');
var groupUtil = require('./groupUtil.js');
var mailUtil = require('./mailUtil');

var renderEventCalendarContent = function(event){
  var groupId = (typeof event.group === "object") ? event.group.id : event.group;
  var content = '<h3>' + event.topic +'</h3>';
  content += '<p>'+event.desc + '</p>';
  content += '<p>'+'For details: http://beehive.eecloud.dynamic.nsn-net.net/group/show/';
  content += groupId+'#/group/'+groupId+'/event/'+event.id+'/show</p>';
  return content;
};


function populateAllUsers(event){
  return event.populateUser()
  .then(users=>{
    event.user = users
    return Promise.resolve(event)
  })
}

function checkIfExist(obj){
  if (!obj){
    return Promise.reject(new Error('obj not find'))
  } else {
    return Promise.resolve(obj)
  }
}

module.exports = {

  createEventObjFromHttp: function(req){

    var newEvent = {};
    newEvent.topic = req.param('Topic');
    newEvent.desc = req.param('EventDetail');
    var strDate1 = req.param('beginDate');
    var kk1 = strDate1.split('-');
    var strTime1 = req.param('BeginTime');
    var tt1 = strTime1.split(':');
    var strDate2 = req.param('endDate');
    var kk2 = strDate2.split('-');
    var strTime2 = req.param('EndTime');
    var tt2 = strTime2.split(':');
    newEvent.begindate = new Date(kk1[0], kk1[1] - 1, kk1[2], tt1[0], tt1[1]);
    newEvent.enddate = new Date(kk2[0], kk2[1] - 1, kk2[2], tt2[0], tt2[1]);
    newEvent.address = req.param('Address');
    newEvent.group = req.param('Group');
    newEvent.tags = req.param('Tag');
    newEvent.owner = req.session.user;
    newEvent.publish = req.param('Publish');
    return newEvent;

  },

  

  addUserToGroup: function(groupid, user, cb) {

    Group
      .find({
        id: groupid
      }).populate('user')
      .exec(function(err, groups) {
        if (err) {
          err = 'Failed to query database with groupid: ' + groupid;
          sails.log.error(err);
          return cb(Error(err));

        } else {

          if (groups.length !== 0) {
            for (var i = 0; i < groups[0].user.length; i++) {
              if (user.id === groups[0].user[i].id) {
                err = 'user existed in group already';
                return cb(null);
              }
            }
            groups[0].user.add(user.id);
            groups[0].save(function(err, s) {
              if (err) {
                console.log('user was failed to add to group:', err);
                return cb(Error(err));
              } else {
                return cb(null,s);
              }

            });

          } else {
            err = 'Failed to find group with groupid:' + groupid;
            sails.log.error(err);
            return cb(Error(err));

          }
        }
      });
  },

  removeUserFromGroup: function(groupid, user, cb) {

    Group
      .find({
        id: groupid
      }).populate('user')
      .exec(function(err, groups) {
        if (err) {
          err = 'Failed to query database with groupid: ' + groupid;
          sails.log.error(err);
          return cb(err);
        } else {
          if (groups.length !== 0) {
            for (var i = 0; i < groups[0].user.length; i++) {
              if (user.id === groups[0].user[i].id) {
                groups[0].user.remove(user.id);
                groups[0].save(function(err, s) {
                  if (err) {
                    err = 'Failed to remove user and save' + user.id;
                    sails.log.err(err);
                    return cb(Error(err));
                  } else {
                    return cb(err);
                  }
                });
              }
            }
          } else {
            err = 'The group is not existed';
            return cb(Error(err));
          }
        }
      });

  },

  

  // event group and id are mandatory to generate a unique mail UID
  // subject is optional: if not specified, default format will be used
  createEventMail: function(ev, subject) {

    function handleImages(html) {

      // TODO: link path in html is hardcoded as it is now to match below img tag:
      // <img src=\"/pic/11522fc5-6359-420f-b484-6cee23d49b98.png\" alt=\"\" />
      var tagImage = /<img ([^>]*)src="(\/pic\/[^>"]*)"([^>]*)>/ig;

      if (html.match(tagImage) != null) {
        return html.replace(tagImage, replacer);
      } else {
        return html;
      }

      function replacer(match, p1, p2, p3) {
        var sprintf = require("sprintf-js").sprintf;
        var DOMAIN_NAME = "http://beehive.eecloud.dynamic.nsn-net.net"; // TODO: get it from env setting

        var newTag = sprintf("<img %s src='%s%s' %s>", p1, DOMAIN_NAME, p2, p3)
        //console.log("Updated tag: " + newTag);

        return newTag;
      }
    }

    

    var event = JSON.parse(JSON.stringify(ev));  // obj deep copy
    var eventDesc = handleImages(event.desc);
    eventDesc =eventDesc.replace(/[\r\n\t]/g, '');
    event.desc = eventDesc;

    var cal = ical({"method": "request"});
    cal.setProdID({
      "company":  "nokia.com",
      "product":  "Beehive",
      "language": "CN"
    });

    var gid = (typeof event.group === "object") ? event.group.id : event.group;

    cal.createEvent({
        // a unique UID must be set for later update/cancellation of this outlook event
        // id: _.pad(event.group, 6, '0') + _.pad(event.id, 6, '0'), // why lodash cannot be used here?
        id: String("000000" + gid).slice(-6) + String("000000" + event.id).slice(-6),

        // sequence number MUST be incremented at every change, use date number instead
        sequence: moment(event.begindate).valueOf(),

        // basic elements of a meeting request
        summary: event.topic,
        start: event.begindate,
        end: event.enddate,
        location: event.address,
        description: event.desc,
    });

    // console.log("\nvEvent: " + JSON.stringify(cal.events()[0]) );

    var mail_obj = {};
    if(!subject) {
      mail_obj.subject = '[Beehive Event] ' + event.topic;
    } else {
      mail_obj.subject = subject;
    }

    mail_obj.from = 'Beehive <I_HZ_MEETUP_FORCES@internal.nsn.com>';
    mail_obj.content = renderEventCalendarContent(event);
    mail_obj.template ='calendarEvent';
    mail_obj.date = new Date();
    mail_obj.alternatives = [{
      contentType: "text/calendar",
      content: cal.toString()
    }];

    return mail_obj;
  },

  sendNotifyMailOnEventCreate: function(event) {
    var publish_notify_mail = this.createEventMail(event);
    return groupUtil.sendNotifyMailToGroupUsers(event.group, publish_notify_mail);
  },

  sendEventMailToUser: function(event, to, subject) {
    var mail_obj = this.createEventMail(event, subject);
    mail_obj.to = to;
    mailUtil.sendNotifyMail(mail_obj);
  },

  addOneUserToEvent: function(user, eventid, cb) {
    return new Promise((resolve, reject)=>{
      Event.findOne({ id: eventid })
      .then(checkIfExist)
      .then(event=>{
        event.userIds = [...new Set([...event.userIds, user._id])]
        return event.save()
      })
      .then((saved)=>cb(null, saved))
      .catch(cb)
    })
  },

  getEventUsersMail: function(event_id, cb){
    var event_mail = [];
    var users;

    Event.find({id:event_id}).populate('user').exec(function(err, events){
      if(err){
          if(cb && (typeof cb==='function')){
              cb(err,null);
          }
      }
      else{
          users = events[0].user;
          var user_num = users.length;
          for(var i=0; i< user_num; i++){
              event_mail.push(users[i].email);    
          }
          if(cb && (typeof cb==='function')){
              cb(null, event_mail);
          }
      }
    });

  },

  sendNotifyMailToEventUsers: function(event_id, mail_obj, cb){
    this.getEventUsersMail(event_id, function(err, event_mail){
      if(err){
          if(cb && (typeof cb==='function')){
              cb(err);
          }
      }
      else{
          mail_obj.to = event_mail;
          mailUtil.sendNotifyMail(mail_obj, cb);
          
      }
    });
  },

  findUserFromTheEvent: function(userid, eventid, cb){
    Event.findOne({id: eventid})
    .then(checkIfExist)
    .then(event=>{
      if(~event.userIds.indexOf(eventid)){
        return populateAllUsers(event)
      } else {
        return Promise.reject(new Error('Could not find user in the event'))
      }
    })
    .then(user=>{
      cb(null, user)
    })
    .catch(cb)
  },

  getCommingEventByGroupid: function(gid) {
    return Event.find({
      group: gid
    }).where({
      enddate: {
        '>=': new Date()
      }
    }).sort({
      "begindate": -1
    })
  },

  getPassedEventByGroupid: function(gid) {
    return Event.find({
      group: gid
    }).where({
      enddate: {
        '<': new Date()
      }
    }).sort({
      "begindate": -1
    })
  },

  addOwnerToEvent: function(event, userId) {
    const newIds = [...new Set([ ...event.userIds, userId]) ]
    event.userIds = newIds
    return event.save()
  }
}
