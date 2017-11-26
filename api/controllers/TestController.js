/**
 * TestController
 *
 * @description :: Server-side logic for managing tests
 * @help        :: See http://links.sailsjs.org/docs/controllers
 */

'use strict';

var testUtil = require('../../lib/testUtil.js');
var _ = require('lodash');

var randomArray = function(arr){
  
  return _.sortBy(arr, function(n){
    var r = _.random(100);
    return r;
  });

};

var sliceFromLodash = function(array, start, end) {
    start || (start = 0);
    if (typeof end == 'undefined') {
      end = array ? array.length : 0;
    }
    var index = -1,
        length = end - start || 0,
        result = Array(length < 0 ? 0 : length);

    while (++index < length) {
      result[index] = array[start + index];
    }
    return result;
};

var createRandomQuestionsListForTest = function(questions, numberForTest){
  var decoratedQuestions = _.map(questions, function(question, index){
    var options = _.map(question.choices, function(choice, index){
      return choice.value;
    });
    var answer = [];
    _.each(options, function(option, key){
      if(option===1){
        answer.push(key);
      }
    });
    _.assign(question, {'index':index});
    _.assign(question, {'answer': answer.join('&')});
    return question;
  });

  var decoratedQuestionsInRandom = randomArray(decoratedQuestions);
  
  if ((numberForTest!=='')&&(numberForTest!==null)&&(!isNaN(numberForTest))){
    if(numberForTest < decoratedQuestionsInRandom.length){
      decoratedQuestionsInRandom = sliceFromLodash(decoratedQuestionsInRandom, 0, numberForTest);
    }  
  }

  return decoratedQuestionsInRandom;

};


module.exports = {
 
  index: function(req, res){

    return res.view('test/index', {layout: null});

  },

  ajaxGetTest: function(req, res){

    var testid = req.param('testid');

    Test.find({id: testid}).populate('paper').exec(function(err, founds){
      if(err){
        return res.json(200, {err: err});
      }else{
        return res.json(200, {test: founds[0]});
      }
    });

  },

  toNewTest: function(req, res){

    var user = req.session.user;
    var groupid = req.param('gid');

    Paper.find({group:groupid}).exec(function(err, papers){
      if(err){ return res.negotiate(err);}
      return res.view('test/NewTest.ejs', {
        papers:papers,
        layout:null,
        groupid: groupid
      });
    });

  },

  doNewTest: function(req, res){

    var user = req.session.user;
    var testname = req.param('testname');
    var groupid = req.param('gid');
    var paperid = req.param('paper');
    var answervisible = req.param('answervisible');
    var limitedtimes = req.param('limitedtimes');
    var numfortest = req.param('numfortest');
    var fromdate = req.param('fromdate');
    var todate = req.param('todate');


    var rules = {};

    rules.answervisible = answervisible;
    rules.numfortest = numfortest;
    rules.fromdate = fromdate;
    rules.todate = todate;
    rules.limitedtimes = limitedtimes;

    var newTestObj = {
      owner: user,
      name: testname,
      paper: paperid,
      rules: JSON.stringify(rules),
      group: groupid
    }

    Test.create(newTestObj, function(err, created){

      if(err){
        return res.negotiate(err); 
      }else{
        return res.redirect('/group/show/'+groupid+'#/group/'+groupid+'/testmanager');
      }

    });

  },

  toManageTest: function(req, res){

    var groupId = req.param('gid');

    Test.find({group:groupId}).populate('paper').populate('owner').exec(function(err, tests){
      if(err){ return res.negotiate(err);}
      return res.view('test/TestManager', {
        tests:tests,
        groupid: groupId,
        layout:null
      });
    });

  },

  toManagePaper: function(req, res){

    var groupid = req.param('gid');

    Paper.find({group:groupid}).populate('owner').exec(function(err, papers){
      if(err){ return res.negotiate(err);}
      return res.view('test/uploadAndDeletePaper', {
        papers:papers,
        groupid: req.param('gid'),
        layout:null
      });
    });

  },


  uploadPaper: function (req, res) {

    var user = req.session.user;
    var paper ={};
    var paperName = req.file('paper')._files[0].stream.filename; 
    paper.name = paperName;
    paper.desc = req.param('paperdesc');
    paper.owner = req.session.user;
    paper.group = req.param('gid');
    paper.numfortest = req.param('questionnumber');

    req.file('paper').upload({
      dirname: sails.config.appPath+'/assets/paper', 
      saveAs: paperName}, 
      function (err, uploadedFiles){
        if (err) {return res.send(500, err);}

        var fs = require('fs');
        fs.readFile('./assets/paper/'+paperName, 'utf8', function(err, data){  
          if(err){
            console.log('file open failed before JSON formate check'+err);
          }
          try{
            var questions = JSON.parse(data);     
          }catch(e){
            console.log(e);
            /* to remove the wrong file */
            fs.unlink('./assets/paper/'+paperName, function(err){
              if(err){console.log(err);}
            });
            return res.json(200, {error: 'JSON format is not right'});
          }

          Paper.create(paper).exec(function(err, createdPaper){
            if(err) { 
              return res.negotiate(err);
            }
            return res.json(200, {username: user.fullname, id: createdPaper.id});
          });

        });     
    });
  },

  toStartTest: function(req, res){

    var groupid = req.param('gid');

    Test.find({group:groupid}).exec(function(err, tests){

      if(err){ return res.negotiate(err);}
      return res.view('test/StartTest', {
        tests:tests,
        layout:null,
        groupid: groupid
      });

    });

  },


  startTest: function(req, res){

    var user = req.session.user;
    var testid = req.param('testid');
    var paperName = req.param('paper');
    var questionNumberForTest = req.param('numfortest');
    var limitedtimes = req.param('limitedtimes');
    var answervisible = req.param('answervisible')||'no';
    var questions;
    var destinQuestions = [];
    var randomIndexList = [];
    var amount = 0;

    Answer.find({test:testid, owner: user.id}).exec(function(err, founds){
      if(err){
        return res.negotiate(err);
      }else{
        if((limitedtimes!=0)&&(founds.length>=limitedtimes)){
          return res.view('test/reject.ejs', {
            err: 'You have reached the maxmium test times: '+ limitedtimes,
            fullname: user.fullname,
            layout:null,
          })
        }else{
          var fs = require('fs');
          fs.readFile('./assets/paper/'+paperName, 'utf8', function(err, data){
            if(err){return res.negotiate(err);}
            try{
              questions = JSON.parse(data);     
            }catch(e){
              console.log(e);
              return res.serverError('JSON.parse was failed, the content of selected paper maybe is not right');
            }
            amount = questions.length;
            destinQuestions = createRandomQuestionsListForTest(questions, questionNumberForTest);
            randomIndexList = _.map(destinQuestions, function(destinQuestion, index){
              return destinQuestion.index;
            });
            var answers = _.map(destinQuestions, function(destinQuestion, index){
              return destinQuestion.answer;
            });
            return res.view('test/RunTest', {
              fullname: user.fullname,
              questions: destinQuestions,
              eid: user.id,
              random_index_list: JSON.stringify(randomIndexList),
              answers: JSON.stringify(answers),
              amount: amount,
              answervisible: answervisible,
              testid: testid
            });
          });
        }
      }
    });
  },

  submitAnswer: function(req, res){

    var user = req.session.user;
    var answers = JSON.parse(req.param('answers'));
    var selects = JSON.parse(req.param('selects'));
    var questionAmount = parseInt(req.param('amount'));
    var randomeIndexs = JSON.parse(req.param('randomindexlist'));
    var score = 0;
    var result = {};
    var position = -1;

    _.each(selects, function(select, index){
      if(select === answers[index]){
        score++;
      }
    });

    score = Math.round((score*100)/answers.length);

    var forIteration = Array(questionAmount);
    var selectsForSerialize = _.map(forIteration, function(n, index){
      position = _.indexOf(randomeIndexs, index);
      if(position>-1){
        return selects[position];
      }
      else{
        return '';
      }
    });
    
    result.paper = req.param('paper');
    result.reply = JSON.stringify(selectsForSerialize);
    result.owner = user || req.param('eid');
    result.score = score;
    result.test = req.param('testid');

    Answer.create(result, function(err, created){
      if(err){
        console.log(err);
        return res.serverError(err);
      }  
      return  res.view('test/FinalResult', {
            fullname: user && user.fullname || req.param('fullname'),
            score: score
          });
      
    });

  },

  destroyTest: function(req, res){
    
    var testId = req.param('testid');
    
    Test.destroy({id: testId}, function(err, deleteds){

      if(err){ return res.negotiate(err);}
      return res.json(200);
    
    });
  },

  destroyPaper: function(req, res){
    var fs = require('fs');
    var paperID = req.param('paperid');
    
    Paper.destroy({id: paperID}, function(err, deleteds){

      if(err){ return res.negotiate(err);}
      if(deleteds.length===0){return res.json(200);}
      
      var deletedPaper = deleteds[0];
      fs.exists('./assets/paper/'+deletedPaper.name, function(existed){
        if(existed){
          fs.unlink('./assets/paper/'+deletedPaper.name, function(err){
            if(err){console.log(err);}
            return res.json(200);
          });
        }else{
          return res.json(200);
        }
      });
      
    });
  },

  showReport: function(req, res){
    var groupId = req.param('gid');

    Test.find({group: groupId}).populate('paper').populate('owner').exec(function(err, tests){
      if(err){
        return res.negotiate(err);
      }else{
        return res.view('test/TestReport.ejs', {
          tests: tests,
          layout: null
        });
      }
    });

  },

  showSimpleReport: function(req, res){

    var testId = req.param('testid');

    Answer.find({test: testId}).populate('owner').exec(function(err, answers){
      if(err){
        return res.negotiate(err);
      }else{
        return res.view('test/SimpleReport.ejs', {
          answers: answers,
          layout: null
        });
      }

    });

  },

  showDetailReport: function(req, res){

    var testId = req.param('testid');

    return res.view('test/DetailReport.ejs', {
          testId: testId,
          layout: null});
    
  },

  getDetailReport: function(req, res){

    var testId = req.param('testid');

    testUtil.buildReport(testId, function(err, questions){
      if(err){
        return res.json(500, err);
      }else{
        return res.json(200, questions);
      }
    });

  }

};

