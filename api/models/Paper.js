/**
* Paper.js
*
* @description :: TODO: You might write a short summary of how this model works and what it represents here.
* @docs        :: http://sailsjs.org/#!documentation/models
*/

module.exports = {

  attributes: {

    name: {
        type: 'string',
    },

    desc: {
        type: 'string'
    },

    owner: {
      model: 'user'
    },

    group: 'integer',

    numfortest: 'integer'

  }
};

