/**
 * User.js
 *
 * @description :: TODO: You might write a short summary of how this model works and what it represents here.
 * @docs        :: http://sailsjs.org/#!documentation/models
 */

module.exports = {

  autoPK: false,

  attributes: {
    fullname: {
      type: 'string',
      defaultsTo: 'Anonymous'
    },

    uid: {
      type: 'string',
    },

    dn: {
      type: 'string'
    },

    email: {
      type: 'email'
    },

    id: {
      type: 'string',
      primaryKey: true,
      unique: true
    },

    userfd: 'string',

    group: {
      collection: 'Group',
      via: 'user'
    },

    events: {
      collection: 'Event',
      via: 'user'
    },

    likedcomments: {
      collection: 'Comment',
      via: 'likeby'
    },

  }
};
