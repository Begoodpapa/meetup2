'use strict';
/*global sails*/
var expect = require('chai').expect;
var supertest = require('supertest');


describe('sails session hack', function() {



  describe('should get to authed folder by session', function() {

    var sessions, app;

    beforeEach(function() {
      sessions = sails.config.session.store.sessions;
      app = sails.hooks.http.app;
    });

    afterEach(function() {
      sails.config.session.store.sessions = {};
    });

    function setSailsSession(key, content) {

      var str = JSON.stringify({
        cookie: JSON.stringify({
          cookie: {
            expires: null,
            path: '/'
          }
        }),
        user: JSON.stringify(content)
      });

      sessions[key] = str;
      return 'sails.sid=testid';
    }

    it('get sails session storage', function(done) {

      var cookie = setSailsSession('testid', {
        fullname: 'name'
      });
      supertest(app)
        .get('/auth/logout')
        .set('Cookie', cookie)
        .expect(302)
        .end(done);

    });
  });


});