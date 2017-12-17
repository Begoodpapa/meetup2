'use strict';
import React from 'react';
import { connect } from 'react-redux';
import { Tabs, Tab, Button, Modal } from "react-bootstrap";
import { BASE_URL } from 'config';
import CommentBox from 'components/comment/comment';
import RegisterMemberModal from 'components/event/registermember';
import EventPublishModal from 'components/event/eventpublish';
import InviteFriendsModal from 'components/event/invitefriends';
var Common = require('../../common.js');
var $ = require('jquery');

class SingleEvent extends React.Component {

  constructor(props) {
    super(props);

    this.state = ({
      event: null,
      showpublishmodal: false,
      showregistermodal: false,
      showinvitemodal: false,
      inevent: false
    })
  }

  showPublish = () => {
    this.setState({
      showpublishmodal: true
    })
  }

  closePublish = () => {
    this.setState({
      showpublishmodal: false
    })
  }

  showRegister = () => {
    this.setState({
      showregistermodal: true
    })
  }

  closeRegister = () => {
    this.setState({
      showregistermodal: false
    })
  }

  showInvite = () => {
    this.setState({
      showinvitemodal: true
    })
  }

  closeInvite = () => {
    this.setState({
      showinvitemodal: false
    })
  }

  getdesc() {
    let desc = this.state.event ? this.state.event.desc : '';
    if(desc.length > 0) {
      $("#eventDesc").html(desc);
    }
  }

  componentDidMount() {
    const {
      groupid,
      eid
    } = this.props;

    var url = BASE_URL + 'group/' + groupid + '/event/' + eid + '/show';
    var that = this;

    $.get(url, function(data, result) {
      if(data.error) {
        //console.log("error received");
        $('#event-details').html('<h3>no event is found</h3>');
      }
      that.setState({
        event: data.event,
        inevent: data.inevent
      })
    })
  }

  getuserlist() {
    if(this.state.event) {
      let userarray = this.state.event.user.map(function(user) {
        return(
          <li key={user.id}>
            <img src={user.userfd ? (BASE_URL + user.userfd) : (BASE_URL + "/images/default_upp.jpg")} alt="..." className="img-circle portrait" id ="nav_user_fd" />
            <a href={BASE_URL + "user/"+user.id + "/profile"}> {user.fullname} </a>
          </li>
        )
      })
      return userarray;
    } else {
      return(
        <li key='0'></li>
      )
    }
  }

  render() {
    const {
      eid,
      groupid,
      auth,
      ownerid
    } = this.props;

    //console.log("event id is:"+eid);    

    if(!eid) {
      return(
        <div>    
          <h4> Invalid Event ID. Please check URL or contact Administrator </h4>          
        </div>
      )
    } else {
      if(this.state.event) {
        var b_dataobj = Common.fulltime(this.state.event.begindate);
        var b_localdate = b_dataobj.localdate;
        var b_fulltime = b_dataobj.fulltime;
      } else {
        var b_localdate = 'loading...';
        var b_fulltime = '';
      }

      if(this.state.event) {
        var e_dataobj = Common.fulltime(this.state.event.enddate);
        var e_localdate = e_dataobj.localdate;
        var e_fulltime = e_dataobj.fulltime;
      } else {
        var e_localdate = 'loading...';
        var e_fulltime = '';
      }

      let hlink = '#/group/show/' + groupid + '/eventedit/' + eid;

      if((auth.authenticated) && (auth.user.id === ownerid)) {
        var isOwner = true;
      } else {
        var isOwner = false;
      }
      //if (auth.authenticated)
      //console.log("fullname is:"+auth.user.fullname);

      let btnText = this.state.inevent ? 'Leave' : 'Join';

      return(

        <div>
          <div className="col-md-9">
            <div className="row">
              <div className="panel panel-default event-content">
                <div className="event-title">
                    <h2 style={{marginTop:'1px', color:'#008000'}}> {this.state.event?this.state.event.topic:''}</h2> 
                      {((this.state.event)&&(this.state.event.publish==true))?
                        (<h5><span className="glyphicon glyphicon-ok">Published</span></h5>):(<div></div>)
                      }
                </div>
                <hr />                
                <div id="event-details">
                  <div id="event_when">
                    <time itemProp="startDate" dateTime="2015-03-14T09:30:00+08:00">                    
                      <span>From:{b_localdate}</span><h4 style={{color:'#800000'}}> {b_fulltime} </h4>                   
                      <span>To:{e_localdate}</span><h4 style={{color:'#800000'}}> {e_fulltime} </h4>
                    </time>
                  </div>
                  <div id="event_where">
                    <span>Address: </span><h4 style = {{color:'#800000'}}>{this.state.event?this.state.event.address:''}</h4>
                  </div>
                  <hr />
                  <div className="event-desc" id="eventDesc">                  
                    {this.getdesc()}
                  </div>
  
                  {/*<a role="button" className="btn btn-default btn-lg" href={hlink}>Edit</a>*/}
                  <Button href={hlink}>Edit</Button>                
                  {
                    ((this.state.event)&&(this.state.event.publish==true))?
                      (<div></div>)
                    :
                    (<Button onClick = {this.showPublish.bind(this)} >Publish</Button>)
                  }                         
                  <EventPublishModal 
                    showModal = {this.state.showpublishmodal}                  
                    closeModal = {this.closePublish}
                    groupid = {groupid} 
                    eid = {eid}
                  />   
                  <label id="errMsgLabel" style={{display:"none"}}></label>
                  <div id="errMsgDiv" style={{display:"none"}}></div>
                </div>              
              </div>
            </div>
            <div className="row">
              <div className="panel panel-default">
                <CommentBox auth={auth} baseUrl={BASE_URL} urlPrefix="comment" category="event" relevantid={eid} />
              </div>
            </div>  
          </div>
        
          <div className="panel panel-default col-md-3">
            <div id="event-attendees">
              <div id="event-tags">
                <br />
                {/* TODO: rewrite it later to make tag function available*/}
              </div>
              <div id="response_box">
                <h3>Welcome</h3>
                {
                  (isOwner)? 
                    <button type="button" className="btn btn-default" onClick={this.showRegister}>Register</button>
                  :                
                    <button type="button" id="userchoice" className={this.state.inevent ? "btn btn-default userleftevent" : "btn btn-default userjoinevent" }>{btnText}</button>                
                }
                <button type="button" className="btn btn-default" onClick={this.showInvite}>Invite</button>
                <RegisterMemberModal 
                  showModal = {this.state.showregistermodal}
                  closeModal = {this.closeRegister}
                  groupid = {groupid}   
                  eid = {eid}                       
                />                
                <InviteFriendsModal
                  showModal = {this.state.showinvitemodal}
                  closeModal = {this.closeInvite}
                  eid = {eid}                   
                />
              </div>
              <div id="join_list">
                <h3>
                <span> {this.state.event?this.state.event.user.length:0} </span>
                <span> going </span>
                </h3>
                <div id="rsp-line" >
                </div>
                <ul id="event-user-list-ul" >
                  {this.getuserlist()}
                </ul>                
              </div>
            </div>
          </div>
        </div>
      )
    }
  }
}

export default connect((state, ownProps) => ({
  auth: state.auth
}))(SingleEvent);