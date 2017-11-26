/**
 * QuestionnaireController
 *
 * @description :: Server-side logic for managing Questionnaire upload ( for both papaer and survey)
 * @help        :: See http://sailsjs.org/#!/documentation/concepts/Controllers
 */

module.exports = {

  index: function(req, res){

    var groupid = req.param('gid');

    return res.view('questionnaire/questionnaire_entry', {
      groupid: req.param('gid'),
      type: req.param('type'),
      layout:null
    });

  },

  show: function (req, res) {

    var groupid = req.param('gid');

    return res.view('questionnaire/questionnaire_main', {
      groupid: req.param('gid'),
      type: req.param('type'),
      layout:null
    });

  },


  create: function(req, res){

    var user = req.session.user;
    var gid = req.param('gid');
    var type = req.param('type');
    var name = req.param('name') + ".json"
    var desc = req.param('desc')
    var data = req.param('data');
    var questionAmount = parseInt(req.param('questionAmount'));

    var questionnaire ={};
    questionnaire.name = name;
    questionnaire.desc = desc;
    questionnaire.owner = user;
    questionnaire.group = gid;

    if( type == 'paper'){
      path = sails.config.appPath+'/assets/paper/'
      questionnaire.numfortest = questionAmount;
    } else{
      path = sails.config.appPath+'/assets/survey/'
    }

    // create file
    var fs = require('fs');
    fs.writeFile( path + name + ".json", JSON.stringify(data),  'utf-8', function( err ){
      if ( err ) {
        console.log(err)
        return res.send(500, err);
      }

      if ( type == 'paper'){
          Paper.create(questionnaire).exec(function(err, createdPaper){
            if(err) {
              return res.negotiate(err);
            }
            return res.json(200, {username: user.fullname, id: createdPaper.id});
          });
      }else{
         Survey.create(questionnaire).exec(function(err, createdSurvey){
           if(err) {
             return res.negotiate(err);
           }
           return res.json(200, {username: user.fullname, id: createdSurvey.id});
         });
      }

    })


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


};

