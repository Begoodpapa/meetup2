import { combineReducers } from 'redux';
import { routerReducer } from 'react-router-redux';

// Reducers
import { authReducer } from 'core/auth';
import { loginmodalReducer } from 'core/loginmodal';
import { pubsubReducer } from 'core/pubsub';
import { groupReducer } from 'core/group';

export default combineReducers({
  loginmodal: loginmodalReducer,
  auth: authReducer,
  routing: routerReducer,
  pubsub: pubsubReducer,
  group: groupReducer,
});
