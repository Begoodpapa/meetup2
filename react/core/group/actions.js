var $ = require('jquery');
import {BASE_URL} from "config" 
import { pubsubActions } from 'core/pubsub';

import {
  GROUP_CREATE_SUCCESS,
  GROUPS_READ_SUCCESS,
  GROUP_UPDATE_SUCCESS  
} from './action-types';

const URLS = {
  GROUP_GET: BASE_URL + 'group/getGroupsAjax',
  GROUP_CREATE: BASE_URL + 'group/createAjax',
  GROUP_UPDATE: BASE_URL + 'group/updateAjax',
  GROUP_DELETE: BASE_URL + 'group/deleteAjax',
}


var $= require('jquery');

$.ajaxSetup({
  crossDomain: true,
  xhrFields: {
      withCredentials: true
  },
});

export function createGroup(data) {
  return (dispatch, getState) => {
    const url = URLS.GROUP_CREATE;
    
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
    const url2 = URLS.GROUP_GET;
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
    const url = URLS.GROUP_UPDATE;
        
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
        const url2 = URLS.GROUP_UPDATE;
        $.get(url2, function(data, result){
            dispatch(readGroups());
        })
  }
}


