/**
* Privilege.js
*
* @description :: TODO: You might write a short summary of how this model works and what it represents here.
* @docs        :: http://sailsjs.org/#!documentation/models
*/

/*  userid: 00000001   administrator
 *  userid: 00000002   actingadministrator
 *  userid: 00000003   globalspecial
 *  userid: 00000004   globaluser
 *  userid: 00000011   groupowner
 *  userid: 00000012   actinggroupowner
 *  userid: 00000013   groupspecial
 *  userid: 00000014   groupuser
 */


module.exports = {

  attributes: {

    userid: 'string',
    
    role:{
      type: 'string',
      defaultsTo: 'user'
    },

    scope:{
      type:'string',
      enum:['global', 'group', 'event'],
      defaultsTo: 'global'
    },

    targetid: 'integer',

  }
};

