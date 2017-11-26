var $ = require('jquery')
import {BASE_URL} from "config" 
import { pubsubActions } from 'core/pubsub';

import {
  SIGN_IN_SUCCESS,
  SIGN_OUT_SUCCESS,
  UPDATE_PROFILE
} from './action-types';


$.ajaxSetup({
  crossDomain: true,
  xhrFields: {
      withCredentials: true
  },
});

export function logout() {
  return (dispatch, getState) => {
    const url = BASE_URL + "auth/logoutAjax"

    $.post(url, "",
      function(data, result){

        dispatch(pubsubActions.notify({level:"success", message: "logout success"}))
        dispatch({
          type: SIGN_OUT_SUCCESS,
        })

    })
  }
}


//mainly for updated the points
export function updateProfile(){
  return (dispatch, getState) => {
        const url2 = BASE_URL + "user/showProfileAjax"
        $.get(url2, function(data, result){
            dispatch({
              type: UPDATE_PROFILE,
              payload: data
            })
        })
  }
}

export function login(data) {

  return (dispatch, getState) => {
    const url = BASE_URL + "auth/loginAjax"

    $.post(url, {uid: data.name, password: data.passwd},
     	function(data, result){   	
        if (data.error){
          dispatch( pubsubActions.notify({ level:"error", message: "Login failure! " + data.error}))
        }else{
          dispatch( pubsubActions.notify({ level:"success", message: "Login success"}))
          dispatch({
            type: SIGN_IN_SUCCESS,
            payload: data
          })

        }
      }
    )
  }

}

export function getAuthStatus(){

  return (dispatch, getState) => {
    const url = BASE_URL + "auth/getStatusAjax"
    $.get(url, function(data, result){
      if(data.err){
        dispatch( pubsubActions.notify({ level:"error", message: data.err}))
      }else{
        dispatch( pubsubActions.notify({ level:"success", message: "get Auth Status success"}))
        dispatch({
            type: SIGN_IN_SUCCESS,
            payload: data
        })
      }

    });
  }
}

