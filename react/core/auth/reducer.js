import {
  SIGN_IN_SUCCESS,
  SIGN_OUT_SUCCESS,
  UPDATE_PROFILE
} from './action-types';

export const initialState = {
  authenticated: false,
  uid: '',
  dn: '',
  fullname: '',
  email: '',
  id: '',
  points: '',
};

export function authReducer(state = initialState, action) {

  switch (action.type) {
    case SIGN_IN_SUCCESS:
      return Object.assign({}, {authenticated: true}, action.payload)

    case SIGN_OUT_SUCCESS:
      return Object.assign({}, {authenticated: false})

    case UPDATE_PROFILE:
      return Object.assign({}, state, action.payload)
    
    default:
      return state
  }
  //return state;
}
