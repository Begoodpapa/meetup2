'use strict';

//assure to close the mailservice before test, otherwise some conflication will happen

var assert = require('assert');
var Promise = require("bluebird")
var testMailTo = 'gang-layner.wang@nokia.com';

describe('MailModel', function() {

  describe('internal function', function() {
    var later = require("later")

    beforeEach(function() {
      return Mail.destroy()
    });
    
    afterEach(function() {
      return Mail.destroy()
    });

    //example/timeperiod.js 
    it('add mail schedule every 20 min', function (done) {
      var message = {"from": "a@a.com",
                    "to": ["a@a.com", "b@b.com"],
                    "subject": "this is test subject",
                    "content": "this is test content",
                    "schedText": "every 20 min",
                    //"date": null                    //Date structure
                    "start": new Date('2000-01-01T00:00:01Z'),
                    "end": new Date('2150-01-01T00:00:01Z')
                    }

      var sched = later.parse.text(message.schedText);
      var expected = new Date()
      var current = new Date()
      
      MailService.addMailSchedText(message)
      .then(function(mailobj){
        Mail.find(function(e,f){
          assert.equal(f.length, 1);
          assert(f[0].schedText, "every 20 min")
          assert(Math.abs((f[0].date.getTime()-(expected.getTime())) < 20*60*1000))
          done();
        });
      });
    });

    it('mail box one need processed', function (done) {
      Mail.create()
      .then(function(createdItem){
          return MailService.checkMailBox()
      })
      .then(function(results){
        assert.equal(results.length, 1)
        results.forEach(function(result){
          assert.ok(result.isFulfilled())
          var item = result.value()
          assert.equal(item.state, "done")
        })
        done()
      })
      .catch(function(error){
        done(error)
      })
    });

    it('mail box one done, one wait', function (done) {
        Mail.create({id:1})
        .then(function(createdMail){
          var current = new Date()
          return Mail.create({id:2, date:new Date(current.getTime()+100000)})
        })
        .then(function(createdItem){
            return MailService.checkMailBox()
        })
        .then(function(results){
          assert.equal(results.length, 2)
          results.forEach(function(result){
            assert.ok(result.isFulfilled())
            var item = result.value()

            if (result.id == 1){
              assert.equal(item.state, "done")
            }else if (result.id == 2){
              assert.equal(item.state, "wait")
            }
          })
          done()
        })
        .catch(function(error){
          done(error)
        })
    });

    it('mail box schedule, at 1:15am', function (done) {
      var message = {"from": "a@a.com",
                    "to": ["a@a.com", "b@b.com"],
                    "subject": "this is test subject",
                    "content": "this is test content",
                    "schedText": "at 1:15 am",
                    }
      var expected1 = new Date('2000-01-01T10:15:00Z');
      var current = new Date();

      MailService.addMailSchedText(message)
      .then(function(addMail){
          return Mail.find()
          .then(function(findMail){
              assert.equal(findMail.length, 1);
              assert(Math.abs((findMail[0].date.getTime()-current.getTime())) < 24*60*60*1000)
              return MailService.checkMailBox()
          })
      })
      .then(function(results){
          assert.equal(results.length, 1)
          results.forEach(function(result){
              assert.ok(result.isFulfilled())
              var item = result.value()
              assert(Math.abs((item.date.getTime()-current.getTime())) < 2*24*60*60*1000)
          })
          done()
      })
      .catch(function(error){
        done(error)
      })
    })

  });


  describe('internal function, test mail render and send email', function(done) {
    beforeEach(function() {
      return Mail.destroy()
    });
    
    afterEach(function() {
      return Mail.destroy()
    });

    it('renderEjs() test mail send', function (done) {
      var content = "You are welcome to join 函数式编程及lodash库介绍 which is on \
        Wed Jan 27 2016 15:30:00 GMT-0500 (EST) http://hzegsav40:80/group/show/20#/event/60/show "

      MailService.renderEjs({id: 1, content: content, layout: null}, function(err, html){
        var message = {from: null,
          to: testMailTo,
          subject: "test message",
          text: html,
          attachments:[{
                        filename: 'Screenshot.png',
                        path: './assets/images/mail_default_head.jpg',
                        cid: 'head@meetup' //same cid value as in the html img src 
          }]
        }

        MailService.sendMail( message.from, 
                              message.to, 
                              message.subject, 
                              message.text, 
                              message.attachments, 
                              null,
                              function(err){
                                done()
                              })
      })
    });

    it('addMailSchedText() add with template should be added', function (done) {
      var message = {"from": "a@a.com",
                    "to": ["a@a.com", "b@b.com"],
                    "subject": "this is test subject",
                    content: "this is test message",
                    template: "mailEvent",
                    "schedText": "every 20 min",
                    "start": new Date('2000-01-01T00:00:01Z'),
                    "end": new Date('2150-01-01T00:00:01Z')
                    }

      MailService.addMailSchedText(message)
      .then(function(mailobj){
        Mail.find(function(e,f){
          assert.equal(f.length, 1);
          assert.equal(f[0].template, "mailEvent")
          done();
        });
      });
    });

    it('renderMail() default template will be renderd', function (done){
      var message = {"from": "a@a.com",
                    "to": ["a@a.com", "b@b.com"],
                    "subject": "this is test subject",
                    "schedText": "every 20 min",
                    content: "this is defalult content",
                    "start": new Date('2000-01-01T00:00:01Z'),
                    "end": new Date('2150-01-01T00:00:01Z')
                    }
      MailService.renderMail(message, function(err, html){
        assert(!err)
        assert(html.search('default template'))
        done()
      })
    })

    it('renderMail() render user defined mail', function (done){

      var eventObj = {};
      eventObj.owner = '10239936';
      eventObj.topic = 'hello from Layner';
      eventObj.desc = 'for test';
      eventObj.group = 1;
      eventObj.begindate = new Date('2016','3','9','14','0');
      eventObj.enddate = new Date('2016','3','9','15','0');
      Event.create(eventObj, function(err, createdEvent){
        var message = {"from": "a@a.com",
                    "to": ["a@a.com", "b@b.com"],
                    "subject": "this is test subject",
                    content: {
                      content: 'this is test message',
                      target: createdEvent,
                      layout: null, 
                    },
                    template: "mail/mailEvent",
                    "schedText": "every 20 min",
                    "start": new Date('2000-01-01T00:00:01Z'),
                    "end": new Date('2150-01-01T00:00:01Z')
                    }

        MailService.renderMail(message, function(err, html){
          assert(!err)
          assert(html.search('mailEvent template')>0);
          assert(html.search('hello from Layner')>0);
          done()
        })

      });
    })

    it('renderMail() render from modal without template', function (done){
      var mailObj = {"from": "a@a.com",
                    "to": ["a@a.com", "b@b.com"],
                    "subject": "this is test subject",
                    "schedText": "every 20 min",
                    content: "this is default content",
                    "start": new Date('2000-01-01T00:00:01Z'),
                    "end": new Date('2150-01-01T00:00:01Z')
                    }
      var renderMailAsync = Promise.promisify(MailService.renderMail)

      MailService.addMailSchedText(mailObj)
      .then(function(){
        return Mail.find()
      })
      .then(function(findMail){
        return renderMailAsync(findMail[0])
      })
      .then(function(html){
        assert(html.search(mailObj.content)>0)
        done()
      })
      .catch(function(err){
        done(err)
      })
    })


    it('renderMail() render from modal with template', function (done){

      var eventObj = {};
      eventObj.owner = '10239936';
      eventObj.topic = 'hello from Layner';
      eventObj.desc = 'for test';
      eventObj.group = 1;
      eventObj.begindate = new Date('2016','3','9','14','0');
      eventObj.enddate = new Date('2016','3','9','15','0');
      Event.create(eventObj, function(err, createdEvent){

        var message = {"from": "a@a.com",
                      "to": ["a@a.com", "b@b.com"],
                      "subject": "this is test subject",
                      content:{
                        content: 'this is test message',
                        target: createdEvent,
                        layout: null, 
                      },
                      template: "mail/mailEvent",
                      attachments: [{
                        filename: 'Screenshot.png',
                        path: './assets/images/mail_default_head.jpg',
                        cid: 'head@meetup' //same cid value as in the html img src 
                      }],
                      "schedText": "every 20 min",
                      "start": new Date('2000-01-01T00:00:01Z'),
                      "end": new Date('2150-01-01T00:00:01Z')
                      }

        MailService.addMailSchedText(message)
        .then(function(mailobj){
          Mail.find(function(e,f){
            MailService.renderMail(f[0], function(err, html){
              assert(!err)
              assert(html.search('mailEvent template')>0)
              done()
            })
          });
        });
      });
    });

    it('renderMailAndSend() check and convert parameters', function(done){
      var message = {"from": "a@a.com",
                    "to": ["a@a.com", "b@b.com"],
                    "subject": "this is test subject",
                    "contentWithTemplate": {
                      content: 'this is test message',
                      layout: null, 
                      template: "mail/mailEvent",
                    },
                    attachments: [{
                      filename: 'Screenshot.png',
                      path: './assets/images/mail_default_head.jpg',
                      cid: 'head@meetup' //same cid value as in the html img src 
                    }],
                    "schedText": "every 20 min",
                    "start": new Date('2000-01-01T00:00:01Z'),
                    "end": new Date('2150-01-01T00:00:01Z')
                    }
      MailService.renderMailAndSend(message, function(err, newobj){
        assert(newobj)
        done()
      })
    });

    it('renderMailAndSend() check and convert parameters from modal', function(done){
      
      var begindate = new Date('2016','3','9','14','0');
      var enddate = new Date('2016','3','9','15','0'); 
      
      var targetObj = {
        owner:'10239936',
        topic:'hello from Layner',
        desc:'for test',
        group:1,
        address: 'HangZhou@26F',
        begindate: begindate,
        enddate: enddate
      };

      var message = {"from": "a@a.com",
                    "to": [testMailTo, "b@b.com"],
                    "subject": "this is test subject",
                    "contentWithTemplate": {
                      content: 'this is test message',
                      target: targetObj,
                      layout: null, 
                      template: "mail/mailEvent",
                    },
                    attachments: [{
                      filename: 'Screenshot.png',
                      path: './assets/images/mail_default_head.jpg',
                      cid: 'head@meetup' //same cid value as in the html img src 
                    }],
                    "schedText": "every 20 min",
                    "start": new Date('2000-01-01T00:00:01Z'),
                    "end": new Date('2150-01-01T00:00:01Z')
                    }


      MailService.addMailSchedText(message)
      .then(function(mailobj){
        Mail.find(function(e,f){
          assert.equal(f.length, 1);
          assert(f[0].attachments)
          MailService.renderMailAndSend(message, function(err, newobj){
            assert(newobj)
            done()
          })
        });
      });
    });

  });

});
