'use strict';

var request = require('supertest');
var path = require('path');
describe('Event uploader', function() {
  var app = null;

  before(function() {
    app = sails.hooks.http.app;
  });


  it('should parse the ics ', function(done) {

    request(app)
      .post('/event/upload')
      .attach('ics', path.join(__dirname, './services/invitation.ics'))
      .field('group', 1)
      .expect(200)
      .end(done);
  });


  it('should return error when no ics attached', function(done) {
    request(app)
      .post('/event/upload')
      .send({
        group: 1
      })
      .expect(400)
      .expect(/No ICS file/)
      .end(done);
  });

});