'use strict';

/**
 * TagController
 *
 * @description :: Server-side logic for managing Tags
 * @help        :: See http://links.sailsjs.org/docs/controllers
 */

module.exports = {

  create: function(req, res) {

    return res.view('tag/TagManager', {
          action: 'new',
          tag: null,
          layout: null,
        });

  },

  new: function(req, res) {

    var newTag = {};
    var user = req.session.user;


    newTag.name = req.param('tagname');
    console.log('tag name:', newTag.name);
    newTag.uplevel = req.param('parenttag');
    newTag.desc = req.param('tagdesc');
    // newTag.uplevel = req.param('parent');
    newTag.uplevel = 0;
    newTag.owner = user;
    newTag.createDate = new Date();
    
    Tag.create(newTag , function(err, created) {

      if(err){
        sails.log.error('Failed to create tag:', err);
        return res.negotiate(err);
      }else{
        var redirectstr = '/tag/show/';
        return res.json(200, {
          redirect: redirectstr
        });
      }
    });
  },

  show: function(req, res) {

    var action = 'show';

    Tag.find({}).exec( function(err, found) {

      if(err){
        sails.log.error('Failed to find tags:', err);
        return res.negotiate(err);
      }else{
        return res.view('tag/TagList', {
          tags: found,
          layout: null,
        });
      }
      
    });

  },

  edit: function(req, res) {


    Tag.find({id:req.param('id')}, function(err, found){

      if(err){
        sails.log.error('Failed to find tags:', err);
        return res.negotiate(err);
      }
      else{

        return res.view('tag/TagManager', {
          action: 'edit',
          tag: found[0],
          layout: null,
        });
      }
    });

  },

  remove: function(req, res) {

    var tagid = req.param('id');
    
    Tag.destroy({id:tagid}).exec(function deleteCB(err){
      
      if(err){
        sails.log.error('Failed to find tags:', err);
        return res.negotiate(err);
      }
      else{
        return res.redirect('/tag/show');
      }

    });

  },

  detach: function(req, res) {
    var eventid = req.param('event');
    var tagid = req.param('tag');

    Event.find({id:eventid}).populate('tags').exec(function(e,r){

      r[0].tags.remove(tagid);
      r[0].save(function(err,s){
        console.log(s.name + 'has been saved');
        return res.redirect('/event/show/'+eventid);
      });

    });
  },

  attach: function(req, res) {

    var eventid = req.param('event');
    var tagid = req.param('tag');

    Event.find({id:eventid}).populate('tags').exec(function(e,r){

      r[0].tags.add(tagid);
      r[0].save(function(err,s){
        console.log(s.name + 'has been saved');
        return res.redirect('/event/show/'+eventid);
      });

    });

  },

  update: function(req, res) {


    var tagid = req.param('id');
    Tag.update(tagid, {
      name: req.param('tagname'),
      desc: req.param('tagdesc'),
      uplevel: req.param('parenttag'),
      owner: req.session.user,
      createDate: new Date(),
    })
    .exec(function(err, updated) {

      if(err){
        sails.log.error('Failed to create tag:', err);
        return res.negotiate(err);
      }else{
        var redirectstr = '/tag/show/';
        return res.json(200, {
          redirect: redirectstr
        });
      }
    });

  }



};

