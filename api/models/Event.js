/**
 * Event.js
 *
 * @description :: TODO: You might write a short summary of how this model works and what it represents here.
 * @docs        :: http://sailsjs.org/#!documentation/models
 */

module.exports = {

  attributes: {

    topic: 'string',
    desc: 'string',
    address: 'string',
    begindate: {
      type: 'datetime',
      before: function(){
        return this.enddate;
      }
    },
    enddate: {
      type: 'datetime',
      after:function(){
        return this.begindate;
      }
    },
    phoDescription: {
      type:'string',
      defaultsTo:'No Description, Add it!'
    },
    group: {
      model: 'group'
    },
    userIds: {
      type: 'array',
      defaultsTo: []
    },
    //user: {
    //  collection: 'user',
    //  via: 'events',
    //  dominant: true
    //},
    photos: {
      collection: 'Photo',
      via: 'album',
    },
    tags: 'string',      //use json string to link the tags, many-to-many relation is too complex.
    owner: {
      model: 'user'
    },
    publish: {
      type: 'boolean',
      defaultsTo: 'false'
    },
    populateUser: function(){ // populate user from userIds
      return User.find({_id: this.userIds})
    }

  }
};
