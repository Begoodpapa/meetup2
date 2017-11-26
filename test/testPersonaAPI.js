'use strict';

var persona = require('../lib/personaUtil.js');

describe('Test the API which used to visit personal', function() {

    
  describe.only('update user score',function(){
    it('update user score', function(done){
        var userid = '10239936';
        var eventid=2;
        var eventname = 'Clean Code Contest';
        var eventlevel=1;
        var score =5;
        var skill = 'Engineering';

        persona.updateScore(userid, skill, eventid, eventname, eventlevel, score, function(err, res, body){
          console.log(res.statusCode);
          if(!err && res.statusCode===200){
            if(body==='score updated successfully'){
              done();
            }
            else{
              done('score updated failed, body');
            }
          }
          else{
            done('score updated failed');
          }
        });      
      });
  });

  describe('add user',function(){
    it('add user to persona from Beehive', function(done){
        var fullname='Wang Gang';
        var uid = 'g12wang';
        var dn = 'employeeNumber=10239936,ou=Internal,ou=People,o=NSN';
        var email = 'gang-layner.wang@nokia.com';
        
        persona.addUser(fullname, uid, dn, email, function(err, res, body){
          console.log(res.statusCode);
          if(!err && res.statusCode===200){
            if(body==='User create successfully'){
              done();
            }
            else{
              done('user added failed, body');
            }
          }
          else{
            done('user added failed');
          }
        });      
      });
  });


});