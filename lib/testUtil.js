'use strict';
var fs = require('fs');
var _ = require('lodash');

module.exports = {

  readPaperByName: function(paperName, cb){

    var filePath =require('path').join(sails.config.appPath,'/assets/paper/',paperName);
    fs.readFile(filePath , 'utf8', function(err, data){
      if(err){return cb(err);}
      try{
        var questions = JSON.parse(data);     
      }catch(e){
        return cb('JSON.parse was failed, the content of selected paper maybe is not right');
      }
      return cb(null, questions);
    });

  },

  readPaperById: function(paperID, cb){
    
    var that = this;
    Paper.find({id:paperID})
    .then(function(foundPapers){
      that.readPaperByName(foundPapers[0].name, cb)
    })
    .catch(function(err){
      cb(err);
    });

  },

  initReport: function(testId, cb){

    var that = this;
    var paperId;

    Test.find({id: testId}, function(err, founds){
      if(err){
        return cb(err, null);
      }else{
        if(founds.length===0){
          return cb('No test was found', null);
        }else{
          paperId = founds[0].paper;
          that.readPaperById(paperId, function(err, questions){
            _.each(questions, function(question, index){
              _.each(question.choices, function(choice, index){
                _.assign(choice, {numOfSelected:0});
              });
            });
            return cb(null, questions);
          });
        }
      }
    });

  },

  buildReport: function(testId, cb){

    var reply, choices;
    var questionsNum;

    var that = this;
    that.initReport(testId, function(err, questions){

      if(err){
        return cb(err, null);
      }

      if(questions.length===0){
        return cb('no question was found',null);
      }

      questionsNum = questions.length;
      
      Answer.find({test:testId}, function(err, answers){
        _.each(answers, function(answer, answerIndex){
          reply = JSON.parse(answer.reply);
          if(reply.length===questionsNum){
            _.each(reply, function(replyOfOneQuestion, questionIndex){
              choices = replyOfOneQuestion.split('&');
              _.each(choices, function(choice, choiceIndex){
                if(choice!==''){
                  questions[questionIndex].choices[choice].numOfSelected++;
                }
              });
            });
          }else{
            return cb('The answer is not consistent with paper', null);
          }
        });
        return cb(null, questions);
      });
    });
  },

};