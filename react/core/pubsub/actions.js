import {BASE_URL} from "config"
//console.log(BASE_URL)

import {
  NOTIFY
} from './action-types';

export function notify(data) {
  return (dispatch, getState) => {
    const { pubsub } = getState();

    pubsub.publish( "NOTIFY",null ,data );

    /* do nothing
    * later change to pure notification system later?*/
    dispatch({
      type: NOTIFY,
      //payload: {key: key}
    })
  }
}

