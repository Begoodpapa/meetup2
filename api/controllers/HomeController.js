'use strict';
/**
 * HomeController
 *
 * @description :: Server-side logic for managing homes
 * @help        :: See http://links.sailsjs.org/docs/controllers
 */
var async = require('async');
var _ = require('lodash');

module.exports = {
  index: function(req, res) {

    var user = req.session.user;
    var GroupSearchString = req.param('GroupSearchString');
    if (!GroupSearchString) {GroupSearchString=''};

     GlobalParam.find({}).exec(function(err, data){
        if (err) {
          sails.log.error(err);
          return res.negotiate(err);
        } else {
          if (data.length === 0){
               GlobalParam.create({visitNumber:1}).exec(function createCB(err, created){
                   sails.log.info('Create the first visit record!');
              });
          }else{
            var now = new Date();
            var newVisitNumber;
            if (now.getDate() - (data[0].updatedAt).getDate() === 1
                || ((now.getDate() === 1) && (now.getMonth() - (data[0].updatedAt).getMonth() === 1)))
             {
                newVisitNumber = 1;
             }else{
                newVisitNumber = data[0].visitNumber+1;
             }
            GlobalParam.update({id: data[0].id},{visitNumber:  newVisitNumber}).exec(function afterwards(err, updated){
                if (err) {
                  sails.log.error(err);
                }
                  sails.log.info('Increase the visit number to ' + updated[0].visitNumber);
                });
          }
        }
     });

    if (GroupSearchString !== ""){
          Group.find({name: {'like': '%'+GroupSearchString+'%'}}).populate('user').exec(function(err, groups) {
              if (err) {
              sails.log.error(err);
              return res.negotiate(err);

            } else {

              var now = new Date();
              return res.view('GroupGalary', {
                findGroups: groups,
                user: user,
                appendix: now.getTime(),
                layout: 'layoutPromote.ejs'
              });
            }
          });
    }else{
      async.waterfall([
      function(callback){
        Group.find({ where: { name: {'like': '%'+GroupSearchString+'%'}},  sort: 'createdAt DESC' }).populate('user').exec(callback) ;
      },

      function(groups, callback){
        var hottedGroups = {},latestGroups={}, resetGroups={};

        latestGroups = groups.slice(0, 3);
        hottedGroups = _.sortBy(groups, function(g){ return 0-g.user.length});
        hottedGroups = hottedGroups.slice(0,3);

        callback(null, latestGroups, hottedGroups, groups);
      },

      ], function(err, latestGroups, hottedGroups, groups){
        if(err){
          sails.log.error(err);
          return res.negotiate(err);
        }else{
          //sails.log.error("latestGroups[%d], hottedGroups[%d], groups[%d] ",latestGroups.length, hottedGroups.length, groups.length);
           var now = new Date();
                  return res.view('GroupGalary', {
                    latestGroups: latestGroups,
                    hottedGroups: hottedGroups,
                    allGroups: groups,
                    findGroups: undefined,
                    user: user,
                    appendix: now.getTime(),
                    layout: 'layoutPromote.ejs'
                  });
        }

    });

  }
},

  calender: function(req, res) {

    Event.find({}, function(err, events) {
      res.view('calender', {
        events: events
      });
    });

  }


};
