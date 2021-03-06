/**
 * Group.js
 *
 * @description :: TODO: You might write a short summary of how this model works and what it represents here.
 * @docs        :: http://sailsjs.org/#!documentation/models
 */

module.exports = {

  attributes: {
    name: {
      type: 'string',
      unique: true
    },
    desc: 'string',
    owner: {
      model: 'user'
    },
    groupfd: 'string',
    user: {
      collection: 'User',
      via: 'group'
    },
    tags:'string',      //use json string to link the tags, many-to-many relation is too complex.
    father: {
      model: 'group'
    }
  }
};
