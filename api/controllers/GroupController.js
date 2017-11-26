'use strict';
/*global Group*/
/**
 * GroupController
 *
 * @description :: Server-side logic for managing groups
 * @help        :: See http://links.sailsjs.org/docs/controllers
 */

var privilegeUtil = require('../../lib/privilegeUtil.js');
var groupUtil = require('../../lib/groupUtil.js');
var groupHeadRoot  = sails.config.upload.groupHead.root;
var fileUtil = require('../../lib/fileUtil.js');
var _ = require('lodash');
var fs = require('fs');
var Promise = require('bluebird');

const {getCommingEventByGroupid, getPassedEventByGroupid} = require('../../lib/eventUtil')

var writeFile = Promise.promisify(fs.writeFile);

function populateAllUsers(group){
  return group.populateUser()
  .then(users=>{
    group.user = users
    return Promise.resolve(group)
  })
}

module.exports = {

  getGroupsAjax: function(req, res){

    function populateAllGroupUsers(allGroups){
      return Promise.all(allGroups.map(populateAllUsers))
    }

    Group.find({sort: 'createdAt DESC' })
    .then(populateAllGroupUsers) //need to refractor in the front end
    .then(allgroups=>{
      const latestGroups = allgroups.slice(0, 3);
      const hottestGroups = allgroups.sort((a, b)=>(b.userIds - a.userIds)).slice(0, 3);
      return Promise.resolve({latestGroups, hottestGroups, allgroups})
    })
    .then(result=>{
      return res.json(200, result);
    })
    .catch(err=>{
      console.error(err)
      return res.json(200, {error: err.message})
    })
  },


  loadoneGroupAjax: function(req, res){

    var groupid = req.param('gid');
    var user = req.session.user;
    let ingroup = false;
    let gro = null;

    //sails.log.info("groupid in req is:"+ groupid);
    //sails.log.info("user in req is:"+ user);
    //

    function checkParams(groupid, user){
      if(!groupid){
        return Promise.reject(new Error(`no such group: ${groupid}`))
      }
      if(!user){
        return Promise.reject(new Error(`no such user: ${user}`))
      }
      return Promise.resolve()
    }

    function ifGroupExist(group){
      if(!group){
        return Promise.reject(new Error(`no group find : ${groupid}`))
      }
      if(~group.userIds.indexOf(user._id)){
        ingroup = true
      }
      gro = group
      return Promise.resolve(group)
    }

    Promise.resolve()
    .then(()=>checkParams(groupid, user))
    .then(()=>Group.findOne({id: groupid}))
    .then(ifGroupExist)
    .then(populateAllUsers)
    .then(()=>Event.find({group: groupid}))
    //.tap(()=>{
    //  Group.find(console.log)
    //  Event.find(console.log)
    //})
    .then(()=>{
      return Promise.all([getCommingEventByGroupid(groupid), getPassedEventByGroupid(groupid)])
    })
    .then(result=>{
      return res.json(200, {
        comingEvents: result[0],
        RecentEvent: result[1][0],
        pastEvents: result[1],
        events: result[0].concat(result[1]),
        group: gro,
        user: user,
        ingroup: ingroup
      })
    })
    .catch(res.negotiate)
  },  
	
  /**
   * `GroupController.create()`
   */
  create: function(req, res) {

    var action = '/newgroup';
    var user = req.session.user;


    Group.find()
    .then(function(groups){
      return res.view('group/GroupManager', {
        title: 'New Group',
        action: action,
        user: user,
        existedGroups: groups
      });
    })
    .catch(function(err){
      return res.view('500', {error: 'Something wrong to get the existed group'+err});
    })

  },

  /**
   * `GroupController.edit()`
   */
  edit: function(req, res) {
    var groupid = req.param('gid');
    var action = '/editGroup/';
    var user = req.session.user;
    Group.findOne({
      id: groupid
    }).populate('owner').exec(function(err, group) {
      if (err) {
        sails.log.error(err);
        return res.negotiate(err);
      } else {
        return res.view('group/GroupManager', {
          title: 'Edit Group',
          action: action,
          group: group,
          user: user
        });
      }
    });

  },

  /**
   * `GroupController.create()`
   */
  remove: function(req, res) {

    var groupid = req.param('gid');
    var deletedGroup;
    Group.findOne({
      id: groupid
    }).exec(function findOneCB(err, found) {
      deletedGroup = found;
    });

    Event.update({
      group: groupid
    }, {
      group: groupid
    }).exec(function afterwards(err, updated) {
      //waiting requirement for how to update event in group deletion case.

      if (err) {
        // handle error here- e.g. `res.serverError(err);`
        sails.log.error('In updating event,');
        sails.log.error(err);
        return;
      }
    });

    Group.destroy({
      id: groupid
    }).exec(function(err, deleted) {
      if (err) {
        sails.log.error(err);
        return res.negotiate(err);
      } else {
        return res.redirect('/');
      }
    });


  },

  /**
   * `GroupController.createAjax()`
   */
  createAjax: function(req, res) {

    let newGroup = {};
    let redirectstr;
    let savedPicFilename = null;

    newGroup.name = req.param('Name');
    newGroup.desc = req.param('Desc');
    newGroup.createDate = new Date();
    newGroup.owner = req.session.user;
    newGroup.father = req.param('Father');

    const userId = req.session.user._id;

    function savePic(picData, filename){
      if (typeof picData !== 'undefined' && picData.length > 0) {
        picData = picData.replace(/^data:image\/\w+;base64,/, "");//get rid of base 64 head, and the leftover is the content of image
        const dataBuffer = new Buffer(picData, 'base64');
        return writeFile(filename, picData);
      }else{
        return Promise.resolve(null);
      }
    }
    const assignPrivilege = Promise.promisify(privilegeUtil.assignPrivilege);

    Group.create(newGroup)
    .then((createdGroup)=>{
      const {id: groupid} = createdGroup;
      newGroup.groupid = groupid;
      redirectstr = `#/group/show/${groupid}/overview`;
      //createdGroup.user.add(userId);
      return groupUtil.add_user_to_group(userId, createdGroup.id )
      //return createdGroup.save();
    })
    .then((createdGroup)=>{
      const picData = req.param('Pic');
      const filename = require('path').join(sails.config.appPath, sails.config.assetsdir.directory, groupHeadRoot) + createdGroup.id + '.jpg';

      return savePic(picData, filename)
      .then(filename=>{
        savedPicFilename = filename;
        return Promise.resolve(createdGroup);
      })
    })
    .then(createdGroup=>{
      const groupFd = groupHeadRoot + createdGroup.id + '.jpg';
      const defautGroupFd = '/images/group_default.jpg';
      return Group.update(createdGroup.id, { groupfd: savedPicFilename?groupFd:defautGroupFd});
    })
    .then(updatedGroups=>{
      return assignPrivilege(newGroup.owner._id, 'groupowner', 'group', newGroup.groupid);
    })
    .then(()=>{
      return res.json(200, {url: redirectstr});
    })
    .catch(err=>{
      //sails.log.error(err);
      return res.json(500, err);
    })
  },


  /**
   * `GroupController.updateAjax()`
   */
  updateAjax: function(req, res) {
    var groupid = req.param('id');
    var group_fd = groupHeadRoot + groupid + '.jpg';
    var picData = req.param('Pic');
    
    var redirectstr = '#/group/show/'+groupid+'/overview';
    // In case the group image is updated, then to create the new group image file to overwrite the existed one.
    // Also to update the groupfd in case user didn't set the group image previously
    if(picData !== undefined && picData.length > 0)
    {
      var fs = require('fs');
      var dataBuffer = new Buffer(picData, 'base64');
      var filename = require('path').join(sails.config.appPath, sails.config.assetsdir.directory, groupHeadRoot) + groupid + '.jpg';
      fs.writeFile(filename, dataBuffer, function(err) {
        if (err) {
          sails.log.error('err');
          return res.json(500, err);
        } else {
          Group.update(groupid, {
            name: req.param('Name'),
            desc: req.param('Desc'),
            groupfd: group_fd,
          }).exec(function(err, updated){
            if (err) {
              sails.log.error('err');
              return res.json(500, err);
            } else {
              return res.json(200, {url: redirectstr});
            }
          });
        }
      });
    }else{
      Group.update(groupid, {
        name: req.param('Name'),
        desc: req.param('Desc'),
      }).exec(function(err, updated){
        if (err) {
          sails.log.error('err');
          return res.json(500, err);
        } else {
          return res.json(200, {url: redirectstr});
        }
      });
    }
  },

  show: function(req, res) {
    var groupid = req.param('id');
    var user = req.session.user;
    var group;
    var ingroup = false;

    async.waterfall([

      function(callback){
        Group.find({
          id: groupid
        }).populate('user').populate('owner').exec(callback);
      },

      function(groups, callback){
        if (groups.length === 0) {
          var err = 'No group is found, groupid: ' + groupid;
          sails.log.error(err);
          callback(err);
        }

        if ((user !== undefined) && (user !== null)) {
          for (var i = 0; i < groups[0].user.length; i++) {
            if (user.id === groups[0].user[i].id) {
              ingroup = true;
              break;
            }
          }
        }
        group = groups[0];
        callback(null, group);
      }

    ], function (err, group) {
      if(err){
        sails.log.error(err);
        return res.negotiate(err);
      }else{
        return res.view('group/GroupInit',{
          group: group,
          user: user,
          ingroup: ingroup,
        });
      }
    });

  },

  loadGroupPic: function(req, res){

    var groupid = req.param('gid');

    async.waterfall([

      function(callback){
        Event.find({
          group: groupid
        }).exec(callback);
      },

      function(events, callback){
        async.map(events,function(event,cb){
          Photo.findAllByAlbum(event.id,cb);
        },callback);
      },

      function(result, callback){
        var photoslink = new Array();
        var x,y;
        for (x in result){
          for (y in result[x].photos){
            photoslink.push(result[x].photos[y].small);
          }
        }
        callback(null, photoslink);
      }
    ], function(err, photoslink){

        return res.json(200, photoslink);

    });

  },

  loadGroup: function(req, res){
    var groupid = req.param('gid');
    var user = req.session.user;

    Group.find({
      id: groupid
    }).populate('user').populate('owner').exec(function(err, groups) {
      if (err) {
        sails.log.error(err);
        return res.negotiate(err);
      }
      if (groups.length === 0) {
        err = 'No group is found, groupid: ' + groupid;
        sails.log.error(err);
        return res.negotiate(err);
      }

      var ingroup = false;

      if ((user !== undefined) && (user !== null)) {
        for (var i = 0; i < groups[0].user.length; i++) {
          if (user.id === groups[0].user[i].id) {
            ingroup = true;
            break;
          }
        }
      }

      var gro = groups[0];

      Event.find({
        group: groupid
      }).where({
        enddate: {
          '>=': new Date()
        }
      }).sort({
        "begindate": -1
      }).populate('user').exec(function(err, events) {
        if (err) {
          err = 'Failed to seach Event with groupid:' + groupid;
          sails.log.error(err);
          return res.negotiate(err);
        }

        var comingEvents = _.sortBy(events, function(o){return o.begindate;});

        Event.find({
          group: groupid
        }).where({
          enddate: {
            '<': new Date()
          }
        }).sort({
          "begindate": -1
        }).populate('user').exec(function(err, pastEvents) {
          if (err) {
            err = 'Failed to seach past event with groupid:' + groupid;
            sails.log.error(err);
            return res.negotiate(err);
          }

          var allEvents = comingEvents.concat(pastEvents);

          return res.view('group/GroupOverview', {
            comingEvents: comingEvents,
            RecentEvent: pastEvents[0],
            pastEvents: pastEvents,
            events: allEvents,
            group: gro,
            user: user,
            ingroup: ingroup,
            layout: null
          });
        });

      });
    });

  },

  showPastEvent: function(req, res){

    var groupid = req.param('gid');

    Event.find({
          group: groupid
        }).where({
          enddate: {
            '<': new Date()
          }
        }).sort({
          "begindate": -1
        }).populate('user').exec(function(err, pastEvents) {
          if (err) {
            err = 'Failed to seach past event with groupid:' + groupid;
            sails.log.error(err);
            return res.negotiate(err);
          }

          return res.view('group/GroupPastEvent', {
            pastEvents: pastEvents,
            group: groupid,
            layout: null
          });
        });

  },

  showComingEvent: function(req, res){

    var groupid = req.param('gid');

    Event.find({
        group: groupid
      }).where({
        enddate: {
          '>=': new Date()
        }
      }).sort({
        "begindate": -1
      }).populate('user').exec(function(err, comingEvents) {
        if (err) {
          err = 'Failed to seach Event with groupid:' + groupid;
          sails.log.error(err);
          return res.negotiate(err);
        }

        return res.view('group/GroupComingEvent', {
            comingEvents: comingEvents,
            group: groupid,
            layout: null
        });
      });

  },

  showCalendar: function(req, res){

    var groupid = req.param('gid');
    
    Event.find({
        group: groupid
      }).sort({
        "begindate": -1
      }).populate('user').exec(function(err, allEvents) {
        if (err) {
          err = 'Failed to seach Event with groupid:' + groupid;
          sails.log.error(err);
          return res.negotiate(err);
        }

        return res.view('group/GroupCalendar', {
            events: allEvents,
            group: groupid,
            layout: null
        });
      });

  },

  showCalendarEvents: function(req, res){

    var groupid = req.param('gid');
    var start = req.param('start');
    var end = req.param('end');

    Event.find({
        group: groupid,
        begindate: { '>' : new Date(start), '<' : new Date(end) }
      }).exec(function(err, durationEvents) {
        if (err) {
          err = 'Failed to seach Event with groupid:' + groupid;
          sails.log.error(err);
          return res.negotiate(err);
        }
        var calendarEvents = [];
        for( var i = 0; i < durationEvents.length; i ++ ){
          calendarEvents.push( {
            title: durationEvents[i].topic,
            start: durationEvents[i].begindate,
            end: durationEvents[i].enddate,
            url: "/group/show/" + groupid + "#/group/" + groupid + "/event/" + durationEvents[i].id + "/show",
          });
        }
        return res.json(calendarEvents);
      });

  },

  find: function(req, res) {
    var limit = 100 || req.param('limit');
    Group.find({})
      .limit(limit)
      .exec(function(err, groups) {
        if (err) {
          sails.log.error('GroupController.search:', err);
          return res.negotiate(err);
        }
        return res.json(groups);
      });

  },

  addUserToGroup: function(req, res) {

    var user = req.session.user;
    var groupid = req.param('gid');


    function checkAddUserToGroupFather(userid, group){
      return new Promise((resolve, reject)=>{
        if(!group.father){
          resolve()
        } else {
          groupUtil.add_user_to_group(userid, group.father)
          .then(userid=>{
            resolve(userid)
          })
          .catch(reject)
        }
      })
    }

    Group.findOne(groupid)
    .catch(err=>{
      throw(new Error(`cant find group, groupid: ${groupid}, user: ${user._id}`))
    })
    .then((group)=>checkAddUserToGroupFather(user._id, group))
    .then(()=>add_user_to_group(user._id, groupid))
    .then(()=>{
      return res.json(200, {ingroup: 'yes'});
    })
    .catch(err=>{
      return res.json(200, {error: err.message});
    })
  },

  removeUserFromGroup: function(req, res) {
    var user = req.session.user;
    var groupid = req.param('gid');

    groupUtil.remove_user_from_group(user._id, groupid)
    .then(()=>res.json(200, {ingroup: 'no'}))
    .catch((err)=>res.joson(200, {error: err.message}))
  },

  showMembers: function(req, res) {

    var groupid = req.param('gid');

    return res.view('group/GroupMembers', {
        gid: groupid,
        layout: null
    });

  },

  getMembersInJson: function(req, res) {

    var groupid = req.param('gid');

    Group.find({id: groupid}).populate('user').exec(function(err, groups) {

      if (err) {
        sails.log.error('GroupController.ShowMembers:', err);
        return res.json(505, err);
      }

      return res.json(200, {
          users: groups[0].user,
          gid: groupid,
          total: groups[0].user.length
      });

    });

  },

  addMembersToGroup: function(req, res){

    var groupid = req.param('gid');
    var member_list = req.param('member_list').split(';');

    /* remove empty string from array first, the empty string
     * will happen when user add ; in the last mail address or user ID
     */
    _.pull(member_list,'');

    async.waterfall([

      function(callback){

        async.map(member_list, LDAPUtils.fuzzySearch, callback);

      },

      function(user_list, callback){

        async.map(user_list, function(entry, cb){
          User.findOrCreate({uid: entry.uid}, {
            uid: entry.uid,
            dn: entry.dn,
            fullname: entry.gecos,
            email: entry.mail,
            id: entry.dn.substr(15,8)
            }, cb);
          }, callback);

      },

      function(user_list, callback){
        groupUtil.addUsersToGroup(user_list.map(usr=>user._id), groupid)
        .then(()=>callback(null))
        .catch(callback)
      }
      ], function(err, results){
      if(err){
        return res.json(200, {error: err.message});
      }
      else{
        return res.json(200);
      }
    });
  },


  importMembersCSVToGroup: function(req, res){

    var path = require('path');
    var XLSX = require('xlsx');
    var fs = require('fs');
    var groupid = req.param('gid');
    var filename = req.file('memberCSVFile')._files[0].stream.filename;
    var member_list = new Array();
    var file = path.join(sails.config.appPath, sails.config.assetsdir.directory, filename);
    var z,y;

    async.waterfall([

      function(callback){
        fs.appendFile(file, req.file('memberCSVFile')._files[0].stream._readableState.buffer[0], function(err){
          if(err){
            console.log("importMembersCSVToGroup appendFil fail " + err);
          }else{
            try{
              var workbook = XLSX.readFile(file);
              var sheet_name_list = workbook.SheetNames;
              sheet_name_list.forEach(function(y) {
                var worksheet = workbook.Sheets[y];
                for (z in worksheet) {
                  if(z[0] === '!') continue;
                  member_list.push(worksheet[z].v);
                }
              });
            }catch(err){
             callback(err);
            }
            callback(null);
          }
        });
      },

      function(callback){
        fs.exists(file, function( exists ){
           if( exists ){
              fs.unlink(file, function(){
              //Console.log('success') ;
              });
           }
        });
        callback(null);
      },

      function(callback){
        async.map(member_list, LDAPUtils.fuzzySearch, callback);
      },

      function(user_list, callback){
        async.map(user_list, function(entry, cb){
          User.findOrCreate({uid: entry.uid}, {
            uid: entry.uid,
            dn: entry.dn,
            fullname: entry.gecos,
            email: entry.mail,
            id: entry.dn.substr(15,8)
            }, cb);
          }, callback);
      },

      function(user_list, callback){
        addUsersToGroup(user_list.map(user=>user._id), groupid)
        .then(()=>callback(null))
        .catch(callback)
      }
      ], function(err, results){
      if(err){
        return res.json(200, {error: err.message});
      }
      else{
        return res.json(200);
      }
    });
  },

  searchUser: function(req, res){

    var groupID= req.param('groupid');
    var searchCriteria;

    try{
      searchCriteria = new RegExp(req.param('search'), 'i');
    }catch(e){
      return res.json(200, 'no user was found');
    }

    Group.findOne({id: groupID})
    .then(populateAllUsers)
    .tap(console.log)
    .then(findGroup=>{
      const filterUsers = findGroup.user
      .filter(user=>searchCriteria.test(user.fullname))
      return res.json(200, {user: filterUsers});
    })
    .catch((err)=>{
      console.log(err)
      return res.json(200, 'no user was found');
    })
  },

  showBigEvent: function(req, res){

    var groupid = 100;
    var user = req.session.user;

    var events = [

      {
        projectName: ['Testing Excellence'],
        projectSlogon: ['Testing is a “Dialog” and happening in anytime and anywhere'],
        projectImage: '/bigevent/test.bmp',
        projectDate: 'May.16',
        projectGroupId: 43
      },

      {
        projectName: ['Cloud CoDe'],
        projectSlogon: ['Let‘s walk in Cloud'],
        projectImage: '/bigevent/Cloud_CoDe.png',
        projectDate: 'May.17',
        projectGroupId: 38
      },

      {
        projectName: ['PDM Excellence'],
        projectSlogon: ['To be the world-class product manager'],
        projectImage: '/bigevent/pdm.png',
        projectDate: 'May.18',
        projectGroupId: 44
      },

      {
        projectName: ['Arch Excellence', 'Innovation','PDM Excellence'],
        projectSlogon: ['Looking back, to meet a better future in architecture','Closer to customer', 'To be the world-class product manager'],
        projectImage: '/bigevent/Thursday.jpg',
        projectDate: 'May.19',
        projectGroupId: 45
      },

      {
        projectName: ['Software Craftsmanship', 'Arch Excellence', 'SCM&CI Excellence', 'Culturosity'],
        projectSlogon: ['MAY THE CRAFTSMANSHIP BE WITH YOU', 'Looking back, to meet a better future in architecture','CI的私房菜', '这个国家不太冷 One day in Poland'],
        projectImage: '/bigevent/Friday.jpg',
        projectDate: 'May.20',
        projectGroupId: 46
      }

    ];

    return res.view('bigevent/index', {
      gid: groupid,
      events: events,
      user: user,
      layout: 'layoutBigEvent.ejs'
    });

  },

  showOpenDay: function(req, res){

    var groupid = 100;
    var user = req.session.user;

    var day1topics = [

      {
        projectImage: '/openday/day1/ChenJianHai.jpg',
        speaker: '陈建海&nbsp;博士',
        info: '云象科技&nbsp;&nbsp;&nbsp;&nbsp;CTO',
        name: '云象联盟区块链技术架构的分享',
      },

      {
        projectImage: '/openday/day1/HuChaoQiang.jpg',
        speaker: '胡超强',
        info: 'NOKIA&nbsp;&nbsp;&nbsp;&nbsp;R&D Specialist',
        name: '物联网小试--10元智能家居解决方案'
        
      },

      {
        projectImage: '/openday/day1/LiBaoCai.jpg',
        speaker: '李保才',
        info: 'NOKIA&nbsp;&nbsp;&nbsp;&nbsp;Senior Specialist',
        name: '5G Overview',
      },

      {
        projectImage: '/openday/day1/PanLiFeng.jpg',
        speaker: '盘礼锋',
        info: 'NOKIA&nbsp;&nbsp;&nbsp;&nbsp;R&D Specialist',
        name: 'Overview of LTE-M'
      },

      {
        projectImage: '/openday/day1/QianYuanSheng.jpg',
        speaker: '钱远盛',
        info: 'NOKIA&nbsp;&nbsp;&nbsp;&nbsp;Chief Architect',
        name: 'RCP 2.0 Architecture introduction'
      },

      {
        projectImage: '/openday/day1/ShuPengFei.jpg',
        speaker: '舒鹏飞',
        info: '由龙信息&nbsp;&nbsp;&nbsp;&nbsp;开发专家',
        name: 'Nodejs程序员的python机器学习之路'
      },

      {
        projectImage: '/openday/day1/WangWei.jpg',
        speaker: '王伟',
        info: 'NOKIA&nbsp;&nbsp;&nbsp;&nbsp;Senior Specialist',
        name: '5G Cloud overview'
      },

      {
        projectImage: '/openday/day1/YangJiaPing.jpg',
        speaker: '杨佳平',
        info: 'NOKIA&nbsp;&nbsp;&nbsp;&nbsp;SW Architect',
        name: 'Cloud BTS 18 Transport solution'
      },

      {
        projectImage: '/openday/day1/ZhangLiaoYuan.jpg',
        speaker: '张燎原',
        info: 'NOKIA&nbsp;&nbsp;&nbsp;&nbsp;Chief Coach',
        name: 'Google I/O 2017 见闻'
      },

      {
        projectImage: '/openday/day1/ZhangYang.jpg',
        speaker: '张杨',
        info: 'NOKIA&nbsp;&nbsp;&nbsp;&nbsp;Development Coach',
        name: '如何避免成为庸众--系统性思考初探',
      }


    ];

    var day2topics = [

      {
        projectImage: '/openday/day2/DaiHeJiang.jpg',
        speaker: '戴和江',
        info: '云铸科技&nbsp;&nbsp;&nbsp;&nbsp;CEO',
        name: '构建研发效能云',
      },

      {
        projectImage: '/openday/day2/GuoMiaoYun.jpg',
        speaker: '郭淼云',
        info: 'NOKIA&nbsp;&nbsp;&nbsp;&nbsp;Technical Leader',
        name: 'Coop Continue Deployment And Service Deployment',
      },

      {
        projectImage: '/openday/day2/LinShuYong.jpg',
        speaker: '林曙湧',
        info: 'NOKIA&nbsp;&nbsp;&nbsp;&nbsp;Test Architect',
        name: 'Cloud testing as a service'
      },

      {
        projectImage: '/openday/day2/QiHongFei.jpg',
        speaker: '齐鸿飞',
        info: 'NOKIA&nbsp;&nbsp;&nbsp;&nbsp;Test Architect',
        name: '测试规划的艺术之路'
      },

      {
        projectImage: '/openday/day2/QingYu.jpg',
        speaker: '秦宇',
        info: '泰克科技&nbsp;&nbsp;&nbsp;&nbsp;应用工程师',
        name: 'Wireless Wonderful--Solutions for IoT Test Challenges'
      },

      {
        projectImage: '/openday/day2/WenShaoHua.jpg',
        speaker: '文少华',
        info: 'Electric Cloud&nbsp;&nbsp;&nbsp;&nbsp;Solution Architect, Certified DevOps Master',
        name: '实战架构持续交付流水线'
      },

      {
        projectImage: '/openday/day2/YangJingFeng.jpg',
        speaker: '杨敬峰',
        info: 'NOKIA&nbsp;&nbsp;&nbsp;&nbsp;Senior Specialist',
        name: 'Ultra Caller Tool: 安卓和IOS手机控制'
      },


      {
        projectImage: '/openday/day2/ZhaoGuoDong.jpg',
        speaker: '赵国栋&nbsp;博士',
        info: '圣点世纪&nbsp;&nbsp;&nbsp;&nbsp;CTO',
        name: '物联网之生物特征识别技术'
      }


    ];

    var day1Agendas = [
      {
        name: '主会场',
        address: 'Zurich',
        topics: [

          {
            name: 'Open Speech and Award',
            speaker: 'Cherry',
            when: '13:00 - 13:30'
          },

          {
            name: 'Google I/O 2017 见闻',
            speaker: '张燎原',
            when: '13:40 - 14:20'
          },

          {
            name: '云象联盟区块链技术架构的分享',
            speaker: '陈建海',
            when: '14:30 - 15:30'
          },

          {
            name: '如何避免成为庸众--系统性思考初探',
            speaker: '张杨',
            when: '15:40 - 17:10'
          }
        ]
      },

      {
        name: '分会场1',
        address: 'Prague',
        topics: [
          {
            name: 'Overview of LTE-M',
            speaker: '盘礼锋',
            when: '13:40 - 14:40'
          },

          {
            name: '5G Cloud overview',
            speaker: '王伟',
            when: '14:50 - 15:50'
          },

          {
            name: 'Nodejs程序员的python机器学习之路',
            speaker: '舒鹏飞',
            when: '16:00 - 16:50'
          }
        ]
      },

      
      {
        name: '分会场2',
        address: 'Brussels',
        topics: [
          {
            name: 'Cloud BTS 18 Transport solution',
            speaker: '杨佳平',
            when: '13:40 - 14:40'
          },

          {
            name: 'RCP 2.0 Architecture introduction',
            speaker: '钱远盛',
            when: '14:50 - 16:20'
          }
        ]
      },

      {
        name: '分会场3',
        address: 'HangZhou',
        topics: [
          {
            name: '5G Overview',
            speaker: '李保才',
            when: '13:30 - 15:30'
          },

          {
            name: '物联网小试--10元智能家居解决方案',
            speaker: '胡超强',
            when: '15:40 - 16:40'
          }
        ]
      }
    ];

    var day2Agendas = [
      {
        name: '分会场1',
        address: 'Prague',
        topics: [
          {
            name: 'Coop Continue Deployment And Service Deployment',
            speaker: '郭淼云',
            when: '13:30 - 14:30'
          },

          {
            name: '实战架构持续交付流水线',
            speaker: '文少华',
            when: '14:40 - 17:10'
          }

        ]
      },

      {
        name: '分会场2',
        address: 'Zurich',
        topics: [
          {
            name: '构建研发效能云',
            speaker: '戴和江',
            when: '13:30 - 14:30'
          },

          {
            name: '物联网之生物特征识别技术',
            speaker: '赵国栋',
            when: '14:40 - 15:20'
          },

          {
            name: 'Wireless Wonderful--Solutions for IoT Test Challenges',
            speaker: '秦宇',
            when: '15:30 - 17:00'
          }
        ]
      },

      {
        name: '分会场3',
        address: 'Brussels',
        topics: [
          {
            name: '测试规划的艺术之路',
            speaker: '齐鸿飞',
            when: '13:30 - 14:30'
          },

          {
            name: 'Cloud testing as a service',
            speaker: '林曙湧',
            when: '14:40 - 15:40'
          },

          {
            name: 'Ultra Caller Tool: 安卓和IOS手机控制',
            speaker: '杨敬峰',
            when: '15:50 - 16:50'
          }
        ]
      }
    ];


    return res.view('openday/index', {
      gid: groupid,
      day1topics: day1topics,
      day2topics: day2topics,
      day1Agendas: day1Agendas,
      day2Agendas: day2Agendas,
      layout: 'layoutOpenDay.ejs'
    });

  },

  uploadImage: function(req, res) {

    var groupID = req.param('groupID');
    var type = req.param('dir');
    var hash = req.param('hash');
    var groupImg = req.file('imgFile');
    var targetDir, dirName, saveAs;

    if( hash){
      targetDir = '/group_' + hash;
    }else{
      targetDir = '/group_' + groupID;
    }

    dirName = require('path').join(sails.config.appPath, sails.config.assetsdir.directory, sails.config.upload.eventpic.root, targetDir);
    saveAs = groupImg._files[0].stream.filename;
    fileUtil.fileUpload(groupImg, dirName, saveAs, function(err){
      if (err) {
        return res.json(200, {error: 1, message: err});
      }else{
        var url =  sails.config.upload.eventpic.root + targetDir + '/'+ saveAs;
        return res.json(200, { error: 0, url: url });
      }
    });

  },

  imageManager: function(req, res){

    var groupID = req.param('groupid');
    var targetDir = '/group_'+groupID;
    var dirName = require('path').join(sails.config.appPath, sails.config.assetsdir.directory, sails.config.upload.eventpic.root, targetDir);

    fileUtil.getAllImages(dirName, function(err, fileList){

      return res.json(200, {current_url: '/pic/group_'+groupID+'/',
        file_list: fileList});

    });

  },

};
