/**
 * SurveyController
 *
 * @description :: Server-side logic for managing surveys
 * @help        :: See http://sailsjs.org/#!/documentation/concepts/Controllers
 */

var surveryUtil = require('../../lib/surveyUtil.js');

module.exports = {

  toManageSurvey: function(req, res){

    var groupid = req.param('gid');

    Survey.find({group:groupid}).populate('owner').exec(function(err, surveys){
      if(err){ return res.negotiate(err);}
      return res.view('survey/uploadAndDeleteSurvey', {
        surveys:surveys,
        groupid: req.param('gid'),
        layout:null
      });
    });

  },

  uploadSurvey: function (req, res) {

    var user = req.session.user;
    var survey ={};
    survey.name = req.file('surveyfile')._files[0].stream.filename;
    survey.desc = req.param('surveydesc');
    survey.owner = req.session.user;
    survey.group = req.param('gid');
    
    req.file('surveyfile').upload({
      dirname: sails.config.appPath+'/assets/survey', 
      saveAs:req.file('surveyfile')._files[0].stream.filename}, 
      function (err, uploadedFiles){
        if (err) {return res.send(500, err);}
        
        Survey.create(survey).exec(function(err, createdSurvey){
          if(err) { 
            return res.negotiate(err);
          }
          return res.json(200, {username: user.fullname, id: createdSurvey.id});
        });

    });
    
  },

  toStartSurvey: function(req, res){

    var groupid = req.param('gid');

    Survey.find({group:groupid}).exec(function(err, surveys){
      if(err){ return res.negotiate(err);}
      return res.view('survey/StartSurvey', {
        surveys:surveys,
        layout:null,
        groupid: req.param('gid')
      });
    });

  },

  startSurvey: function(req, res){

    var user = req.session.user;
    var surveyID = req.param('survey');
    var paging = req.param('paging');
    var questions;
    var amount = 0;

    async.waterfall([
      function(callback) {
        Survey.find({id:surveyID}, callback);
      },

      function(foundsurveys, callback) {
        if(foundsurveys.length===0){
          callback('no survey was found');
        }else{
          var surveyName = foundsurveys[0].name;
          var fs = require('fs');
          fs.readFile('./assets/survey/'+surveyName, 'utf8', callback);
        }
      }], function(err, data){

        if(err){return res.negotiate(err);}
        try{
          questions = JSON.parse(data);     
        }catch(e){
          return res.serverError('JSON.parse was failed, the content of selected survey maybe is not right');
        }
        amount = questions.length;

        if(paging==='0'){
          return res.view('survey/RunSurveyInOnePage', {
            fullname: user.fullname,
            questions: questions,
            eid: user.id,
            surveyid: surveyID,
            amount: amount
          });

        }else if(paging ==='1'){
          return res.view('survey/RunSurveyInPaging', {
            fullname: user.fullname,
            questions: questions,
            eid: user.id,
            surveyid: surveyID,
            amount: amount
          });

        }
        

      });

  },

  submitSurvey: function(req, res){

    var user = req.session.user;
    var selects = JSON.parse(req.param('selects'));
    var questionAmount = parseInt(req.param('amount'));
    var surveyID = req.param('survey');
    var result = {};
    
    
    result.survey = surveyID;
    result.reply = JSON.stringify(selects);
    result.owner = user;
    result.score = 0;

    Feedback.create(result, function(err, created){
      if(err){
        console.log(err);
        return res.serverError(err);
      }  
      return  res.view('survey/SurveyResult', {
            fullname: user.fullname,
            surveyID: surveyID
          });
      
    });

  },

  toGetReport: function(req, res){

    var groupid = req.param('gid');

    Survey.find({group:groupid}).exec(function(err, surveys){
      if(err){ return res.negotiate(err);}
      return res.view('survey/ToGetSurveyReport', {
        surveys:surveys,
        layout:null,
        groupid: req.param('gid')
      });
    });

  },

  getReport: function(req, res){
    var surveyId = req.param('surveyid');
    var reportType = req.param('surveytype');

    Feedback.find({survey: surveyId}).populate('owner').exec(function(err, feedbacks){
      if(err){
        return res.negotiate(err);
      }else{
        if(reportType==='0'){
          return res.view('survey/SurveyReport.ejs', {
            feedbacks: feedbacks
          });
        }else if(reportType==='1'){
          return res.view('survey/DetailReport.ejs', {
          surveyid: surveyId});
        }else{
          return res.negotiate('report type is not right');
        }
      }
    });

  },

  getDetailReportData: function(req, res){

    var surveyId = req.param('surveyid');

    surveryUtil.buildReport(surveyId, function(err, questions){
      if(err){
        return res.json(500, err);
      }else{
        return res.json(200, questions);
      }
    });

  },

  destroySurvey: function(req, res){
    var fs = require('fs');
    var surveyID = req.param('surveyid');
    
    Survey.destroy({id: surveyID}, function(err, deleteds){

      if(err){ return res.negotiate(err);}
      if(deleteds.length===0){return res.json(200);}
      
      var deletedSurvey = deleteds[0];
      fs.exists('./assets/survey/'+deletedSurvey.name, function(existed){
        if(existed){
          fs.unlink('./assets/survey/'+deletedSurvey.name, function(err){
            if(err){console.log(err);}
            return res.json(200);
          });
        }else{
          return res.json(200);
        }
      });
      
    });
  },
	
};

