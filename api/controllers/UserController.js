/**
 * UserController
 *
 * @description :: Server-side logic for managing users
 * @help        :: See http://links.sailsjs.org/docs/controllers
 */

'use strict';
var portraitRoot = sails.config.upload.portrait.root;
var privilegeUtil = require('../../lib/privilegeUtil.js');

function checkIfExist(obj){
  if (!obj){
    return Promise.reject(new Error('obj not find'))
  } else {
    return Promise.resolve(obj)
  }
}

module.exports = {


	showMyEvent: function(req, res) {

		var user = req.session.user;

		User.find({
			id: user.id
		}).populate('events').exec(function(err, users) {
			if (err) {
				return res.negotiate(err);
			} else {
				var events = users[0].events;
				return res.view('event/MyCalendar', {
					events: events,
					user: user,
				});
			}
		});
	},
	
	showMyEventAjax: function(req, res) {
	  var user = req.session.user;
	  //console.log(' showMyEventAjax user id:%s', user._id);
    User.findOne({_id: user._id})
    .then(checkIfExist)
    .then(user=>{
      return Event.find({userIds: user._id})
    })
    .then(events=>{
	    return res.json(200, {
	      events: events,
	      user: user,
	    });				
    })
    .catch(()=>{
	    return res.json(200, {error: "Failed to seach events"});
    })
	},	

	showMyGroup: function(req, res) {

		var user = req.session.user;

		User.find({
			id: user.id
		}).populate('group').exec(function(err, users) {

			if (err) {
				sails.log.error(err);
				return res.negotiate(err);
			} else {
				var groups = users[0].group;

				var now = new Date();
				res.view('user/MyGroup', {
					groups: groups,
					user: user,
					appendix: now.getTime(),
					layout: 'layoutPromote.ejs'
				});

			}

		});

	},
	

	showMyGroupAjax: function(req, res) {
		const user = req.session.user;

    User.findOne({_id: user._id})
    .then(checkIfExist)
    .then(user=>{
      return Group.find({userIds: user._id})
    })
    .then(group=>{
	    return res.json(200, {
	      groups: group,
	      user: user,
	    });				
    })
    .catch(()=>{
	    return res.json(200, {error: "Failed to seach groups"});
    })


	},

	showProfile: function(req, res) {
		var uid = req.param('uid');
    var user = req.session.user;
    var isAdministrator = false;

		User.findOne({
			id: uid
		}).exec(function(err, found) {
			if (err) {
				sails.log.error(err);
				return res.negotiate(err);
			} else {
          if(user){
            privilegeUtil.getPrivilege(user.id, 'global', null, function(err, privileges){
              
              if(!err){
                if((privileges[0])&&(privileges[0].role==='administrator')){
                  isAdministrator = true;
                }
              }
              return res.view('user/profile', {
                user: found,
                isLoginUser: false,
                isAdministrator: isAdministrator,
                layout: null
              });

            });
          }else{
            return res.view('user/profile', {
              user: found,
              isLoginUser: false,
              isAdministrator: isAdministrator,
              layout: null
            });
          }
			}
		});
	},

	showMyProfile: function(req, res) {
		var user = req.session.user;
		var isAdministrator = false;
		var userfound = {};

		async.waterfall([

      function(callback){
      	if(user!=null){
      		User.findOne({uid: user.uid}, callback);
      	}else{
      		callback("user is null");
      	}
      },

      function(found, callback){
      	sails.log(found);
        if(found){
        	userfound = found;
          privilegeUtil.getPrivilege(found.id, 'global', null, callback);
        }else{
          callback('not find the user');
        }
      },

      function(userPrivilege,callback){
      	sails.log(userPrivilege);
				if(userPrivilege[0]){
					Role.find({name:userPrivilege[0].role}, function(err, found){
						if(found[0]){
							if(found[0].admincontrol === 'yes'){
								isAdministrator = true;
							}
						}
						callback(null);
					});
				}else{
					callback(null);
				}
      },

      function(callback){
      	callback(null, userfound, isAdministrator );
      }

    ], function(err, user, isAdministrator){
      if(err){
      	sails.log.error(err);
				return res.negotiate(err);
      }else{
				return res.view('user/MyProfile', {
					user: user,
					isAdministrator: isAdministrator,
					isLoginUser: true
				});
      }
    });

	},

	updateProfilePicture: function(req, res) {
		var user = req.session.user;
		var postData = req.param('Pic');
		var fs = require('fs');
		var path = require('path');
		var user_fd = portraitRoot + user.uid + '.jpg';
		var filename = path.join(sails.config.appPath, sails.config.assetsdir.directory, user_fd);
		var dataBuffer = new Buffer(postData, 'base64');
		fs.writeFile(filename, dataBuffer, function(err) {
			if (err) {
				sails.log.error(err);
				return res.negotiate(err);
			}else{
				User.update(user.id, {
					userfd: user_fd,
				}).exec(function(err, updated) {
					if (err) {
						sails.log.error(err);
						return res.negotiate(err);
					} else {
						var redirectstr = '/user/myprofile';
						return res.json(200);
					}
				});
			}
		});
	}

};
