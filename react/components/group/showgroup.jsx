import React from 'react';
import { Col } from "react-bootstrap";
import { connect } from 'react-redux';
import { groupActions } from 'core/group';
import Groupsidebar from 'components/group/groupsidebar';
import ComingEvents from 'components/event/comingevents';
import PastEvents from 'components/event/pastevents';
import FullCalendar from 'components/group/fullcalendar';
import GroupOverview from 'components/group/overview';
import SingleEvent from 'components/event/event';
import GroupMembers from 'components/group/members';
import EventMgr from "components/event/eventmanager"; //for adding and editing an event
import DownLoad from "components/file/download";
import FileMgr from "components/file/filemanager";
import { BASE_URL } from 'config';
import { NavDropdown, MenuItem } from 'react-bootstrap';

require('../../../assets/vender/dropzone/dist/min/basic.min.css');
require('../../../assets/vender/dropzone/dist/min/dropzone.min.css');
require('../../../assets/vender/blueimp-gallery/css/blueimp-gallery.min.css');
require('../../../assets/vender/blueimp-bootstrap-image-gallery/css/bootstrap-image-gallery.min.css');
require('../../../assets/vender/fuelux/dist/css/fuelux.min.css');
require('../../../assets/styles/beehive.css');
require('../../../assets/styles/questionnaire.css');
require('../../../assets/js/requirejs/require.min.js'); { <script type="text/javascript" src="/js/config.js?b7924afd"></script> }
var $ = require('jquery');

class ShowGroup extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      pastEvents: [],
      comingEvents: [],
      events: [],
      RecentEvent: {},
      ownername: '',
      owneremail: '',
      ownerid: '',
      groupdesc: '',
      ingroup: false,
      currenttag: this.props.params.contentTag
    }
  }

  getgid() {

    const {
      params
    } = this.props;

    var gid = params.groupId;

    //console.log("gid is:"+gid);   
    return gid;
  }

  gettag() {

    const {
      params
    } = this.props;

    var tag = params.contentTag;

    //console.log("tag is:"+tag);   
    return tag;
  }

  loadonegroup(gid) {
    const url = BASE_URL + "group/" + gid + "/loadoneGroupAjax";

    //console.log("url is:"+url);       
    const that = this;

    $.get(url, function(data, result) {
      that.setState({
        pastEvents: data.pastEvents,
        comingEvents: data.comingEvents,
        RecentEvent: data.RecentEvent,
        events: data.events,
        ownername: data.group.owner.fullname,
        owneremail: data.group.owner.email,
        ownerid: data.group.owner.id,
        groupdesc: data.group.desc,
        userfd: data.group.owner.userfd,
        ingroup: data.ingroup
      })

      //console.log("111groupdesc is:"+data.group.desc);        
    })
  }

  componentDidMount() {
    window.scrollTo(0, 0);
    var gid = this.getgid();
    this.loadonegroup(gid);
  }

  componentDidUpdate() {
    window.scrollTo(0, 0);
  }

  componentWillReceiveProps(nextProps) {
    //console.log('componentWillReceiveProps, nextProps is:',nextProps);
    if((nextProps.auth.authenticated) && (!this.props.auth.authenticated)) {
      //console.log('from non-authenticated to authenticated');
      var gid = this.getgid();
      this.loadonegroup(gid);
    }

    //console.log("nextProps tag is:"+nextProps.params.contentTag);
    //console.log("this.state.currenttag is:"+this.state.currenttag);    
    if(nextProps.params.contentTag != this.state.currenttag) {
      this.setState({
        currenttag: nextProps.params.contentTag
      })
    }
  }

  render() {
    const {
      auth,
      allgroups,
    } = this.props;

    var head_group_name, groupowner_fullname, groupfd = '';
    var num_members = 0;
    var groupid = this.getgid();
    var joingroup = ((this.state.ingroup) && (auth.authenticated)) ? 'Leave us' : 'Join us!';

    var tag = this.gettag();

    //console.log("current tag in render is:"+this.state.currenttag);
    //console.log("this.gettag result is:"+tag);

    if(tag === 'overview') { //show overview of a group
      var renderByTag = (
        <GroupOverview
          groupdesc = {this.state.groupdesc}
          pastEvents = {this.state.pastEvents}
          comingEvents = {this.state.comingEvents}
          RecentEvent = {this.state.RecentEvent}
          events = {this.state.events}
          groupid = {groupid}
        />
      )
    } else if(tag === 'member') { //show all members of a group
      var renderByTag = (
        <GroupMembers
          groupid = {groupid}
        />
      )
    } else if(tag === 'pastevent') { //show all past events of a group
      var renderByTag = (
        <PastEvents
          groupid = {groupid}
          pastEvents = {this.state.pastEvents}
        />
      )
    } else if(tag === 'comingevent') { //show all coming events of a group
      var renderByTag = (
        <ComingEvents
          groupid = {groupid}
          comingEvents = {this.state.comingEvents}
        />
      )
    } else if(tag === 'calendar') { //show all events by a calendar view
      var renderByTag = (
        <FullCalendar
          groupid = {groupid}
          events = {this.state.events}
        />
      )
    } else if(tag === 'eventshow') { //show details of a single event          
      var renderByTag = (
        <SingleEvent
          groupid = {groupid}
          eid = {this.props.params.eid}
          ownerid = {this.state.ownerid}  
        />
      )
    } else if(tag === 'eventadd') { //add a single event          
      var renderByTag = (
        <EventMgr
          groupid = {groupid}
          eid = {this.props.params.eid}
          ownerid = {this.state.ownerid}  
          action = 'add'
        />
      )
    } else if(tag === 'eventedit') { //edit a single event          
      var renderByTag = (
        <EventMgr
          groupid = {groupid}
          eid = {this.props.params.eid}
          ownerid = {this.state.ownerid}
          action = 'edit'
        />
      )
    } else if(tag === 'todownloadfile') {
      var renderByTag = (
        <DownLoad
          groupid = {groupid}
        />
      )
    } else if(tag === 'filemanage') {
      var renderByTag = (
        <FileMgr
          groupid = {groupid}
        />
      )
    }

    //get corresponding group name        
    $.each(allgroups, function(i, field) {

      var id = field.id;

      if(id == groupid) {
        head_group_name = field.name;
        groupowner_fullname = field.owner; //TODO replace with name later, because field.owner is actually owner id
        groupfd = field.groupfd;
        num_members = field.userIds.length;

        return false;
      }
    });

    return(
      <Col className="page" md={12} sm={12}>
      <div className="fuelux">
        <div id ="main">
          <div className="container-fluid">
            <div className="row">
              <div className="col-md-12">
                {/*<a href="#/group/<%= group.id%>/load" title="">*/}
                <a href={'#/group/show/' + groupid + '/overview'} title="">
                  <h1 className="group-h1 group-name-span" id="head_group_name">
                    {head_group_name}
                  </h1>
                </a>
              </div>
            </div>
            <div className="row">
              <div className="col-md-12">
                <nav className="navbar navbar-default" role="navigation">
                  <div className="container-fluid">
                                  
                    <div className="navbar-header">
                      <button type="button" className="navbar-toggle collapsed" data-toggle="collapse" data-target="#group-navbar-collapse" aria-expanded="false" aria-controls="group-navbar-collapse">
                        <span className="sr-only">Toggle navigation</span>
                        <span className="icon-bar"></span>
                        <span className="icon-bar"></span>
                        <span className="icon-bar"></span>
                      </button>
                    </div>
                    
                    <div className="collapse navbar-collapse" id="group-navbar-collapse">
                      <ul className="nav navbar-nav">                   
                        <li className="active"><a href={'#/group/show/'+groupid+'/overview'} data-target={'#group/show/'+groupid+'/overview'}>Home<span className="sr-only">(current)</span></a></li>
                        <li><a href={'#/group/show/'+groupid+'/member'} id="memebers">Members</a></li>                                                                        
                        <NavDropdown eventKey={1} title="File" id="file-nav-dropdown">
                          <MenuItem href={'#/group/show/'+groupid+'/todownloadfile'} eventKey={1.1}>File Download</MenuItem>
                          <MenuItem href={'#/group/show/'+groupid+'/filemanage'} eventKey={1.2}>File Manage</MenuItem>
                        </NavDropdown>                        
                        <li><a href={'#/group/'+groupid+'/tags'}>Tags</a></li>                        
                      </ul>
                      <ul className="nav navbar-nav nav-pills navbar-right">
                        <li><a href={'#/group/show/' + groupid + '/eventadd'}>New Event</a></li>
                        <a id="joingroup" role="button" className="btn btn-primary navbar-btn pull-right">{joingroup}</a>                        
                      </ul>                      
                    </div>             
                  </div>
                </nav>         
              </div>
            </div>
            <br />
            <div className="row">
              <div className="col-md-12">
                <div className="row">
                  <div id="sidebar" className="col-md-3 col-xs-6">
                    <Groupsidebar 
                      groupname={head_group_name} 
                      groupowner_fullname={this.state.ownername} 
                      groupowner_email ={this.state.owneremail}
                      ownerid = {this.state.ownerid}
                      groupfd={groupfd}
                      num_members={num_members}
                      pastEvents={this.state.pastEvents}
                      comingEvents={this.state.comingEvents}
                      events={this.state.events}
                      userfd={this.state.userfd}
                      groupid = {groupid}
                    />
                  </div>              
                  <div className="col-md-9 col-xs-6" >
                    {renderByTag}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
    </div>
  </Col>

    )
  }
}

export default connect((state, ownProps) => ({
  allgroups: state.group.allGroups,
  auth: state.auth
}), groupActions)(ShowGroup);