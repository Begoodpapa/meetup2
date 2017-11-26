'use strict';
var fs = require('fs');
var _ = require('lodash');

module.exports = {

  readSurveyByName: function(surveyName, cb){

    var filePath =require('path').join(sails.config.appPath,'/assets/survey/',surveyName);
    fs.readFile(filePath , 'utf8', function(err, data){
      if(err){return cb(err);}
      try{
        var questions = JSON.parse(data);     
      }catch(e){
        return cb('JSON.parse was failed, the content of selected survey maybe is not right');
      }
      return cb(null, questions);
    });

  },

  readSurveyById: function(surveyID, cb){
    
    var that = this;
    Survey.find({id:surveyID})
    .then(function(foundSurveys){
      that.readSurveyByName(foundSurveys[0].name, cb)
    })
    .catch(function(err){
      cb(err);
    });

  },

  initReport: function(surveyID, cb){

    var that = this;

    that.readSurveyById(surveyID, function(err, questions){
      _.each(questions, function(question, index){
        var selects = new Array(question.choices.length);
        _.each(selects, function(select, index){
          selects[index] = 0;
        })
        _.assign(question, {selects:selects});
      });
      cb(null, questions);
    });
        
  },

  buildReport: function(surveyID, cb){

    var reply, choices;
    var questionsNum;

    var that = this;
    that.initReport(surveyID, function(err, questions){

      questionsNum = questions.length;
      
      Feedback.find({survey:surveyID}, function(err, feedbacks){
        _.each(feedbacks, function(feedback, feedbackIndex){
          reply = JSON.parse(feedback.reply);
          if(reply.length===questionsNum){
            _.each(reply, function(replyOfOneQuestion, questionIndex){
              choices = replyOfOneQuestion.split('&');
              _.each(choices, function(choice, choiceIndex){
                if(choice!==''){
                  questions[questionIndex].selects[choice]++;
                }
              });
            });
          }
        });
        cb(null, questions);
      });
    });
  },

};