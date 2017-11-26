/*
 * node-imap for receiving email: https://github.com/mscdex/node-imap
 * mailparser for parsing received emails
 *
 * TODO: avoid creating duplicate events based on emails by
 * 1) fetch and mark as read (doesn't work), or fetch since (last email UID + 1)
 * 2) or save event digest for duplication checking, or use db unique constraint (subject + starttime)...
 */
'use strict';

var Imap = require('imap'),
    mailparser = require("mailparser"),
    fs = require('fs');

var IMAPServer = 'webmail.nsn-intra.net'; 
var imap = new Imap({
  user: (sails.config.function_mail) ? sails.config.function_mail.user : 'username',
  password: (sails.config.function_mail) ? sails.config.function_mail.password : 'password',
  host: IMAPServer,
  port: 993,
  tls: true,
  debug: console.log
  });

var events = require('events');
function AsyncEmitter() {
  events.EventEmitter.call(this);
}

require('util').inherits(AsyncEmitter, events.EventEmitter);
var emitter = new AsyncEmitter();
emitter.setMaxListeners(50);

var user;
emitter.on("mailReady", function(email, vcal) {
  User.findOne({email: email}, function(err, found) {
    if (err || found === undefined) {
      //console.log('User not found');
      emitter.emit("userNotFound", email, vcal);
    } else {
      //console.log("User exists: " + JSON.stringify(found));
      user = found;
      emitter.emit("userFoundOrCreated", user, vcal);
    }
  });

});

emitter.on("userNotFound", function(email, vcal) {
  LDAPUtils.fuzzySearch(email, function(err, entry) {
    if (err) {
      //return console.log("User not found in LDAP" + err.message);
    }

    User.create({
      uid: entry.uid,
      dn: entry.dn,
      fullname: entry.gecos,
      email: entry.mail,
      id: entry.dn.substr(15,8)
    }, function(err, created) {
      if (err) {
        //return console.log("Failed to create user: " + err.message);
      } else {
        user = created;
        //console.log("Created user: " + JSON.stringify(user));
        emitter.emit("userFoundOrCreated", user, vcal);
      }
    });
  });

});

emitter.on("userFoundOrCreated", function(user, vcal) {
  ICSParse.vcal2Event(vcal, function(err, event) {
    if (err) {
      return sails.log.error('Failed to parse vcalendar content:', err.message);
    }

    //console.log("ICSParse.vcal2Event: " + JSON.stringify(event) );
    emitter.emit("veventReady", event, user);
  });
});

// final step
emitter.on("veventReady", function(event, user) {    
    //console.log("Create event for user: " + JSON.stringify(user) );

    Event.create({ 
      topic: event.topic,
      desc: event.desc,
      begindate: event.start,
      enddate: event.end,
      address: event.address,
      group: { id: 2 },
      owner: { id: ( (user === undefined) ? null: user.id) }, 
    }, function(err, event) {
      if (err) {
        sails.log.error('Failed to create event:', err.message);
      } else {
        console.log("Email event created: " + JSON.stringify(event));
      }
    });  
});

emitter.on("error", function(error) {
  sails.log.error(err.message);
});

module.exports = {
  startService: function() {

    function _checkMail() {
      MailReceiver.checkIncomingMail();
    }

    var later = require('later');
    var textSched = later.parse.text('every 30 sec');
    later.setInterval(_checkMail, textSched);
  },

  checkIncomingMail: function() {
    var openInbox = function(cb) {
      imap.openBox('Inbox', true, cb);
    };

    imap.once('ready', function() {
      openInbox(function(err, box) {
        if (err) {
          sails.log.error(err.message);
          return;
        }

        // search latest new mails
        imap.search([ 'NEW' ], function(err, results) {
          if (err) {
            sails.log.error(err.message);
            return;
          }

          if (!results || (Array.isArray(results) && results.length === 0)) {
            console.log("No unread mail.");
            return;
          }

        var f = imap.fetch(results, {
          bodies: '',
          markSeen: true // Mark messages as read when fetched to avoid creating duplicated events
        });

        f.on('message', function(msg, seqno) {
          var fds, filenames, parser;
          fds = {};
          filenames = {};

          parser = new mailparser.MailParser({
            streamAttachments: true,
            //debug: true,  // other options: unescapeSMTP, defaultCharset, showAttachmentLinks
          });

          parser.on("headers", function(headers) {
            //return console.log("Headers: " + JSON.stringify(headers));
          });

          parser.on("end", function(mail) {
            if(mail.hasOwnProperty("alternatives")) {
              //console.log("Received meeting request:" + mail.alternatives[0]["content"]);              
              emitter.emit("mailReady", mail.from[0].address, mail.alternatives[0]["content"]);
            } else {
              //console.log("Ignore non meeting email: " + mail.subject);
            }

            return;
          });

          // only listen when streamAttachments: true
          // TODO: add attachment to event
          parser.on("attachment", function(attachment, mail) {
            //var output = fs.createWriteStream(attachment.generatedFileName);
            //attachment.stream.pipe(output);
            return console.log("parser.on:attachment:" + attachment.generatedFileName);
          });

          msg.on("body", function(stream, info) {
            //console.log("on:body:" + info.which);
            
            stream.on('data', function(chunk) {
              //console.log("on:body:data");
              return parser.write(chunk.toString('utf8'));
            });

            stream.on('end', function(chunk) {
              //console.log("on:body:end");
              return parser.end();  // send end event to parser
            });
          });

          msg.once("attributes", function(attributes) {
            //return console.log("on:attributes: [[[" + JSON.stringify(attributes) + "]]]");
          });

          msg.once('end', function() {
            //console.log("on:end");
          });
        });

        f.once('error', function(err) {
          console.log('Fetch error: ' + err);
        });

        f.once('end', function() {
          //console.log('Done fetching all messages!');
          imap.end();
        });
      }); // end of search
      }); // end of openBox
    });

    imap.once('error', function(err) {
      console.log(err);
    });

    imap.once('end', function() {
      //console.log('Connection ended');
    });

    imap.connect();

  },

};


