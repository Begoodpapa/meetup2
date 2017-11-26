'use strict';
var surveyAndTestUtil = require('../lib/testUtil.js');
var assert = require('assert');


describe('Get the report of one test or survey', function(){

  describe.only('Read paper, init report and build report', function(){

    var paperID;

    beforeEach(function(done){
      Paper.destroy()
      .then(function(){
        return Answer.destroy();
      })
      .then(function(){
        var paper ={};
        paper.name = 'for_test.json';
        paper.desc = 'for test';
        paper.owner = '10239936';
        paper.group = 1;
        paper.numfortest = 5;
        return Paper.create(paper);
      })
      .then(function(createdPaper){
        var answer_obj = {};
        paperID = createdPaper.id;
        answer_obj.paper = createdPaper.id;
        answer_obj.owner = '10239936';
        answer_obj.reply = '[\"1\",\"0&1&2&3\",\"1\",\"4\",\"2\"]';
        answer_obj.score = 50;
        return Answer.create(answer_obj);
      })
      .then(function(createdAnswer){
        var answer_obj = {};
        answer_obj.paper = paperID;
        answer_obj.owner = '10239936';
        answer_obj.reply = '[\"0\",\"2&3\",\"3\",\"2\",\"3\"]';
        answer_obj.score = 50;
        return Answer.create(answer_obj);
      })
      .then(function(createdAnswer){
        done();
      })
      .catch(function(err){
        done(err);
      })
    });

    it('readPaperByName', function(done){

      surveyAndTestUtil.readPaperByName('for_test.json', function(err, questions){
        if(err){
          done(err);
        }else{
          done();
        }
      })

    });

    it('initReport', function(done){
      
      surveyAndTestUtil.initReport(paperID, function(err, questions){
        assert.equal(questions.length, 5);
        done();
      })

    });

    it('buildReport', function(done){

      surveyAndTestUtil.buildReport(paperID, function(err, questions){
        assert.equal(questions[0].choices[0].numOfSelected, 1);
        assert.equal(questions[0].choices[1].numOfSelected, 1);
        assert.equal(questions[0].choices[2].numOfSelected, 0);
        assert.equal(questions[0].choices[3].numOfSelected, 0);
        assert.equal(questions[1].choices[0].numOfSelected, 1);
        assert.equal(questions[1].choices[1].numOfSelected, 1);
        assert.equal(questions[1].choices[2].numOfSelected, 2);
        assert.equal(questions[1].choices[3].numOfSelected, 2);
        done();
      })

    });

  });

});