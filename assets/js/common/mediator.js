'use strict'

define(function(){
  
  var _msg = {};

  return {
    register: function(type, action){
      if(_msg[type]){
        _msg[type].push(action);
      }else{
        _msg[type] = [];
        _msg[type].push(action);
      }
    },

    send: function(type, arg){
      if(_msg[type]){
        for(var i= 0, len = _msg[type].length; i<len; i++){
          _msg[type][i]&&_msg[type][i](arg);
        }
      }
    }
  }

});