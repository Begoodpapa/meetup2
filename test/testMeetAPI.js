'use strict';
var expect = require('chai').expect;
var supertest = require('supertest');

describe('MeetAPI', function() {

  var app;

  before(function() {
    app = sails.hooks.http.app;
  });

  it('GET /meet', function(done) {
    supertest(sails.hooks.http.app)
      .get('/meet')
      .expect(200)
      .end(function(err, res) {
        expect(res.body).to.deep.equal([]);
        done(err);
      });
  });

});