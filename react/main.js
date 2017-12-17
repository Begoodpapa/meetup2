import React from 'react';
import { render } from 'react-dom';
import { Root } from './components/root';
import { browserHistory } from 'react-router';
import { syncHistoryWithStore } from 'react-router-redux';
import { getAuthStatus } from './core/auth/actions.js';
import { readGroups } from './core/group/actions.js';
import configureStore from './store';
var $ = require('jquery');
import { Thumbnail, Col } from "react-bootstrap";

var PubSub = require('pubsubjs');

const store = configureStore({ pubsub: PubSub.create() });

const history = syncHistoryWithStore(browserHistory, store);

store.dispatch(readGroups());
store.dispatch(getAuthStatus());

// disable warnning from editor see https://github.com/facebook/draft-js/issues/53
console.error = (function() {
  var error = console.error
  return function(exception) {
    if((exception + '').indexOf('Warning: A component is `contentEditable`') != 0) {
      error.apply(console, arguments)
    }
  }
})()

render(<Root history={history} store={store}/>, document.getElementById('app'));