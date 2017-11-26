var $ = require('jquery')
import {BASE_URL} from "config"
//console.log(BASE_URL)

import {
  OPEN_LOGIN_MODAL,
  CLOSE_LOGIN_MODAL,
} from './action-types';

export function openLoginModal() {
  return (dispatch, getState) => {
    dispatch({
      type: OPEN_LOGIN_MODAL,
      //payload: {key: key}
    })
  }
}

export function closeLoginModal() {
  return (dispatch, getState) => {
    dispatch({
      type: CLOSE_LOGIN_MODAL,
      //payload: {key: key}
    })
  }
}

