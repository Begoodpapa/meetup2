import React, { Component, PropTypes } from 'react';
import { Route, Router, IndexRoute, hashHistory } from 'react-router';
import { Provider } from 'react-redux';
import NavApp from './nav/nav';
import MyComponent from './notification';
import Main from "./index";
import MyProfile from "./profile";
import MyGroup from "./mygroup";
import MyEvent from "./myevent";
import GroupSR from "./group/searchresult";
import GroupMgr from "./group/groupmanager";
import EventMgr from "./event/eventmanager";
import { Col } from "react-bootstrap";

import ShowGroup from './group/showgroup';
import Footer from './footer/footer';
import { openLoginModal } from '../core/loginmodal/actions';

class Wrap extends Component {
  render() {
    return(
      <div>
        <NavApp/>
        <MyComponent/>
        {this.props.children}
      </div>
    )
  }
}

export class Root extends Component {
  static propTypes = {
    store: PropTypes.object.isRequired
  };

  requireAuth(nextState, replace) {

    const { store, router } = this.props;
    const { auth } = store.getState();
    console.log('require Auth');
    if(!auth.authenticated) {
      hashHistory.goBack();
      store.dispatch(openLoginModal());
    }
  }

  render() {

    const { store } = this.props;

    return(
      <Provider store={store}> 
        <Router history={hashHistory}>
          <Route path="/" component={Wrap}>
            <IndexRoute component={Main} />
            <Route path="myprofile" component={MyProfile}/>
            <Route path="mygroup" component={MyGroup}/>
            <Route path="myevent" component={MyEvent}/>
            <Route path="groupsr/:groupId/(:groupName)" component={GroupSR}/> //the componet to put group search result
            //contentTag is one of [overview, member, pastevent, comingevent, calendar, eventshow, eventadd, eventedit, todownloadfile, filemanage]
            <Route path="group/show/:groupId/:contentTag(/:eid)" component={ShowGroup}/>
            //oprTag is one of [new,edit]
            <Route path="group/manage/:oprTag(/:groupId)" component={GroupMgr}/>
          </Route>
        </Router>
      </Provider>
    );
  }
}