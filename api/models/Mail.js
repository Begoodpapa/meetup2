/**
* Mail.js
*
* @description :: TODO: You might write a short summary of how this model works and what it represents here.
* @docs        :: http://sailsjs.org/#!documentation/models
*/

module.exports = {

  attributes: {

    // mail content
    to:{
        type:'array'
    },
    subject:'string',
    content: {
        type: "json",
        defaultsTo: null
    },

    template: {
      type: "string",
      defaultsTo: null
    },
    attachments: {
        type: "json",
        defaultsTo: null
    },
    alternatives: {
        type: "json",
        defaultsTo: null
    },
    //mail control
    schedText:{
      type: 'string',
      defaultsTo: null
    },

    date:{
      type: 'datetime',
      defaultsTo: new Date()
    },

    state:{
        type: 'string',
        enum: ['wait', 'sending', 'done', 'failed'],
        defaultsTo:'wait'
    },
    retrytimes:{
        type:'int',
        defaultsTo:0
    },
    loginfo:'string'
  }
};


