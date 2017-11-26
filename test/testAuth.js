'use strict';
var should = require('should');
var supertest = require('supertest');

describe('LDAP auth', function() {
  it('should log faile with empty uid either password', function(done) {

    supertest(sails.hooks.http.app)
      .post('/auth/login')
      //.expect(400)
      .end(function (err, res) {
      	console.log("\nresp:" + sails.hooks.http.response);
      	res.text.should.containEql('Redirecting to /login');
        done(err);
      });
  });

  it('should log failed with only uid ', function(done) {
    supertest(sails.hooks.http.app)
      .post('/auth/login')
      .send({
        uid: 'pshu'
      })
      //.expect(400)
      .end(function(err, res) {
      	res.text.should.containEql('Redirecting to /login');
        done(err);
      });
  });

  //it.skip('should log failed with wrong password ', function(done) {
  it('should log failed with wrong password ', function(done) {
    supertest(sails.hooks.http.app)
      .post('/auth/login')
      .send({
        uid: 'pshu',
        password: 'Xsomepassword'
      })
      //.expect(200)
      .end(function(err, res) {
        res.text.should.containEql('Redirecting to /login');
        done(err);
      });
  });
});

