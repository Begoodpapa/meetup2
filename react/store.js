import { applyMiddleware, compose, createStore } from 'redux';
import thunk from 'redux-thunk';
import createLogger from 'redux-logger';

import reducer from './reducer';

export default (initialState = {}) => {
  let finalCreateStore;

  const logger = createLogger();
  if (process.env.NODE_ENV !== 'production') {
    // configure redux-devtools-extension
    // @see https://github.com/zalmoxisus/redux-devtools-extension
    finalCreateStore = compose(
      applyMiddleware(thunk/*, logger*/),
      window.devToolsExtension ? window.devToolsExtension() : f => f,
    )(createStore);
  }
  else {
    finalCreateStore = compose(
      applyMiddleware(thunk),
      //window.devToolsExtension ? window.devToolsExtension() : f => f,      
    )(createStore);
  }


  const store = finalCreateStore(reducer, initialState);
  if (module.hot) {
    module.hot.accept('./reducer', () => {
      store.replaceReducer(require('./reducer').default);
    });
  }

  return store;
};
