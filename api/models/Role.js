'use strict';
/**
 * Role.js
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

    isDefaultRole:{
      type: 'string',
      enum: ['yes', 'no'],
      defaultsTo: 'no'
    },

    scope:{
      type:'string',
      enum:['global', 'group', 'event'],
      defaultsTo: 'global'
    },

    deletegroup:{
      type: 'string',
      enum: ['yes', 'no'],
      defaultsTo: 'no'
    },

    editgroup:{
      type:'string',
      enum: ['yes', 'no'],
      defaultsTo: 'no'
    },

    deleteevent:{
      type: 'string',
      enum: ['yes','no'],
      defaultsTo: 'no'
    },

    editevent:{
      type: 'string',
      enum:['yes', 'no'],
      defaultsTo: 'no'
    },

    publishevent:{
      type: 'string',
      enum:['yes', 'no'],
      defaultsTo: 'no'
    },

    addgroupmember:{
      type: 'string',
      enum: ['yes', 'no'],
      defaultsTo: 'no'
    },

    deletegroupmember:{
      type: 'string',
      enum: ['yes', 'no'],
      defaultsTo: 'no'
    },

    exportgroupmember:{
      type: 'string',
      enum:['yes', 'no'],
      defaultsTo: 'no'
    },

    addeventmember:{
      type: 'string',
      enum:['yes', 'no'],
      defaultsTo: 'no'
    },

    deleteeventmember:{
      type: 'string',
      enum:['yes', 'no'],
      defaultsTo: 'no'
    },

    exporteventmember:{
      type:'string',
      enum:['yes','no'],
      defaultsTo:'no'
    },

    uploadpaper:{
      type: 'string',
      enum: ['yes','no'],
      defaultsTo: 'no'
    },

    deletepaper:{
      type: 'string',
      enum: ['yes', 'no'],
      defaultsTo: 'no'
    },

    gettestreport:{
      type: 'string',
      enum: ['yes', 'no'],
      defaultsTo: 'no'
    },

    createtag:{
      type: 'string',
      enum:['yes', 'no'],
      defaultsTo: 'yes'
    },

    deletetag:{
      type: 'string',
      enum: ['yes', 'no'],
      defaultsTo: 'no'
    },

    deletefile:{
      type: 'string',
      enum: ['yes', 'no'],
      defaultsTo: 'no'
    },

    deletetest:{
      type: 'string',
      enum: ['yes', 'no'],
      defaultsTo: 'no'
    },

    admincontrol:{
      type: 'string',
      enum: ['yes', 'no'],
      defaultsTo: 'no'
    },
  }
};