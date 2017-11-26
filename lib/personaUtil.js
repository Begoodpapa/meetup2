'use strict';

var _request = require('request');

var request = _request.defaults({
  headers: {
    'Content-Type': 'application/json',
  }
});


module.exports = {

  updateScore: function(userid, skill, eventid, eventname, eventlevel, score, cb){

    request.post(sails.config.persona.server+'/score/createfromthirdpart', {
      json: {
      userid: userid,
      skill: skill,
      eventid: eventid,
      eventname: eventname,
      eventlevel: eventlevel,
      score: score}}, function(err, res, body){
      cb(err, res, body);
    });

  },

  addUser: function(fullname, uid, dn, email, cb) {
  
    request.post(sails.config.persona.server+'/user/createfromthirdpart', {
      json:{
        fullname: fullname,
        uid: uid,
        dn: dn,
        email: email}}, function(err, res, body){
          cb(err, res, body);
    });
  
  }


};
