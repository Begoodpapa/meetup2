var $ = require('jquery');
import {BASE_URL} from "config" 
import { pubsubActions } from 'core/pubsub';

import {
  GROUP_CREATE_SUCCESS,
  GROUPS_READ_SUCCESS,
  GROUP_UPDATE_SUCCESS  
} from './action-types';

var $= require('jquery');

$.ajaxSetup({
  crossDomain: true,
  xhrFields: {
      withCredentials: true
  },
});

export function createGroup(data) {
  return (dispatch, getState) => {
    const url = BASE_URL + "group/createAjax";  
    
    var redirectUrl = '';
    
		$.ajax({  
      type : "post",  
      url : url,  
      data : data,  
      async : false,  
      dataType : "json",
      success : function(resdata){  
        dispatch(pubsubActions.notify({level:"success", message: "Create the new group success"}));
        dispatch(readGroups());  
        
        redirectUrl = resdata.url;
      }, 
      error : function(resdata, result){
	      dispatch(pubsubActions.notify({level:"error", message: "Failed to create new group."}));
      }
    });  
    return redirectUrl;
  }  
}

export function readGroups(){
  return (dispatch, getState) => {
    const url2 = BASE_URL + "Group/getGroupsAjax";
    $.get(url2, function(data, result){
        dispatch({
          type: GROUPS_READ_SUCCESS,
          payload: data
        })
    })
  }
}

export function updateGroup(data){
  return (dispatch, getState) => {
    const url = BASE_URL + "group/updateAjax";
        
    var redirectUrl = '';
    
		$.ajax({  
      type : "post",  
      url : url,  
      data : data,  
      async : false,  
      dataType : "json",
      success : function(resdata){  
        dispatch(pubsubActions.notify({level:"success", message: "Update the group success"}));
        
        
 				dispatch({
          type: GROUP_UPDATE_SUCCESS,
          payload: data
        })
    
        redirectUrl = resdata.url;
      }, 
      error : function(resdata, result){
	      dispatch(pubsubActions.notify({level:"error", message: "Failed to updat the group."}));
      }
    });  
    return redirectUrl;        
        
  }
}

export function deleteGroup(){
  return (dispatch, getState) => {
        const url2 = BASE_URL + "group/deleteAjax";
        $.get(url2, function(data, result){
            dispatch(readGroups());
        })
  }
}


