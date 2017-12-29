'user strict';

var mailUtil = require('./mailUtil');
var Promise = require('bluebird');

module.exports = {
  
  //Get users list for a certain group
  getGroupUsersMail: function(groupId){

    function checkAndPopulateUser(group){
      if(!group){
        return Promise.reject(new Error(`no such group, groupId: ${groupId}`))
      } else {
        return group.populateUser()
      }
    }

    return new Promise((resolve, reject)=>{
      Group.findOne({id: groupId})
      .then(checkAndPopulateUser)
      .then(users=> resolve(users.map(user=> user.email)))
      .catch(reject)
    })
  },
  
  //Check whether a user belongs to a certain group
  findUserFromTheGroup: function(userid, groupId, cb){

    function checkAndPopulateUser(group){
      if(!group){
        return Promise.reject(new Error(`no such group, groupId: ${groupId}`))
      } else {
        return group.populateUser()
      }
    }

    return new Promise((resolve, reject)=>{
      Group.findOne({id: groupId})
      .then(checkAndPopulateUser)
      .then(users=> {
        return Promise.resolve( users.find(user=> user._id === userid))
      })
      .then(user=>{
        if(!user){
          reject(new Error(`Could not find user in the group groupid:${groupId}, userid: ${userid}`))
        }else{
          resolve(user)
        }
      })
      .catch(reject)
    })

  },

  //Add a new user to a certain group
  add_user_to_group: function(userId, groupId) {
    return new Promise((resolve, reject)=>{
      Group.findOne({id: groupId})
      .then(group=> {
        if(!group){
           reject(new Error(`no such group, groupId: ${groupId}`))
        } else {
          const findUserId = group.userIds.find(id=> id===userId)
          if(findUserId){
            resolve(userId)
          } else {
            group.userIds = [...group.userIds, userId] //append the new userId
            group.save()
            .then(()=>resolve(userId))
          }
        }
      })
    })
  },

  //Add a list of new users to a certain group
  addUsersToGroup: function(userIds, groupId) {
    return new Promise((resolve, reject)=>{
      Group.findOne({id: groupId})
      .then(group=> {
        if(!group){
           reject(new Error(`no such group, groupId: ${groupId}`))
        } else {
          const newIds = [...new Set([ ...group.userIds, ...userIds]) ] 
          group.userIds = newIds
          group.save()
          .then(()=>resolve(group))
        }
      })
    })
  },

  //remove a user from a certain group 
  remove_user_from_group : function(userId, groupId, cb) {
    return new Promise((resolve, reject)=>{
      Group.findOne({id: groupId})
      .then(group=> {
        if(!group){
           reject(new Error(`no such group, groupId: ${groupId}`))
        } else {
          const findUserIdIndex = group.userIds.indexOf(userId)
          if(!~findUserIdIndex){
           reject(new Error(`user not in the group, groupId: ${groupId}, userId: ${userId}`))
          } else {
            group.userIds.splice(findUserIdIndex, 1)
            group.save()
            .then(()=>resolve(userId))
          }
        }
      })
    })

  },

  //Send a notification mail to users of a certain group
  sendNotifyMailToGroupUsers: function(group_id, mail_obj){
    const sendNotifyMail = Promise.promisify(mailUtil.sendNotifyMail)

    return this.getGroupUsersMail(group_id)
    .then(group_mail=>{
      mail_obj.to = group_mail;
      return sendNotifyMail(mail_obj)
    });
  },
};
