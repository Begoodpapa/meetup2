/**
 * Comment.js
 *
 * @description :: TODO: You might write a short summary of how this model works and what it represents here.
 * @docs        :: http://sailsjs.org/#!documentation/models
 */

module.exports = {

  attributes: {
    content: {
      type: 'string',
    },

    likecount: {
      type: 'integer',
    },

    likeby: {
      collection: 'User',
      via: 'likedcomments'
    },

    createdby: {
      model: 'User'
    },

    category: {
      type: 'string',
      enum: ['request', 'service', 'event']
    },

    //relevantid is the id of which the comment belong to, 
    //it can be one request id or service id
    relevantid: {
      type: 'string',
    },

    replyto: {
      model: 'Comment',
    },

    maincomment: {
      model: 'Comment',
    },
  }
};
