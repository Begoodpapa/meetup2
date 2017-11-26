'use strict';
import React from 'react';
import {connect} from 'react-redux';
import {Button, ButtonGroup, Modal, Col, Form, FormGroup, FormControl, ControlLabel, SplitButton, MenuItem} from "react-bootstrap";
import {BASE_URL} from 'config';
var $ = require('jquery');

class InviteFriendsModal extends React.Component{
  constructor(props){
    super(props);
  } 
  
  changeEmail = ()=>{
  	this.hideAlertMsg();
  }
  
  hideAlertMsg()
  {
    if(!$('#input_check_alert').hasClass('hidden'))
    {
      $('#input_check_alert').toggleClass('hidden');
    }
  };

  showAlertMsg(message)
  {
    if(!message)
    {
      message = 'Server or Network error.';
    }
    var dt = '<dt>'.concat(message, '</dt>');
    $('#input_check_alert > dl').html(dt);
    $('#input_check_alert').removeClass('hidden');
  };  
  
  btnClick(){

    var btn = $(this);
    this.hideAlertMsg();

    var prefix = $('#friend_email').val().trim();
    var postfix = $('#mailpostfix').val().trim()
    var input = prefix + "@" + postfix;
    if((prefix.length==0) || (postfix.length==0)) {
      this.showAlertMsg("Pls provide a valid email address.");
      return;
    }

    var email = input;
    if (input.indexOf('@') !== -1) {
      var found = input.match(/\S+@(nokia|nokia-sbell)\.com$/i);
      if (!found) {
        this.showAlertMsg("Pls provide a valid Nokia/NSB email.");
        return;
      }
    } else {
      email = input + "@nokia.com";
    }

    var eid = this.props.eid;
    var that = this;
    
    $.post(BASE_URL + 'event/'+eid+'/InviteFriendAjax', {
      'email': email,
      'from': $('#from').val()
    }).done(function(data) {
        if(data.error) {
          this.showAlertMsg(data.error);
	       } else {	       
	          that.showAlertMsg("Invitation sent out successfully.");
	          return;
	          //window.location.reload();
	        }
      })
      .fail(function(){
        this.showAlertMsg();
      })
      .always(function(){
        btn.button('reset');
      });    	
  }
  
  render(){
  	return(
			<Modal show = {this.props.showModal} onHide={this.props.closeModal} bsSize="lg">			
				<Modal.Header closeButton>
				  <Modal.Title>Invite a friend to the event</Modal.Title>				
				</Modal.Header>
				<Modal.Body>
          <div id="input_check_alert" className="alert alert-danger hidden" role="alert">
            <dl>
            </dl>
          </div>				
	        <div className="input-group">
	          <input type="text" id="friend_email" className="form-control" placeholder="Your friend's email" aria-describedby="basic-addon2" onKeyUp={this.changeEmail} />
	          <span className="input-group-addon" id="basic-addon2">@</span>
	          <input type="text" id="mailpostfix" className="form-control" defaultValue="nokia-sbell.com" placeholder="nokia-sbell.com" aria-describedby="basic-addon2" onKeyUp={this.changeEmail} />
	        </div>
	
	        <input id="eventid" type="hidden" value=""></input>
	        <input id="from" type="hidden" value={this.props.auth.authenticated&&this.props.auth.user.fullname}></input>	          									
				</Modal.Body>
	  		<Modal.Footer>
	        <Button type="submit" onClick = {this.btnClick.bind(this)}>
	          Invite
	        </Button>	 
	        <Button type="button" onClick = {this.props.closeModal}>
	          Close
	        </Button>			        
	  		</Modal.Footer>				
			</Modal>	  	  
    )
  }
}

export default connect((state, ownProps) => ({
	auth: state.auth
}))(InviteFriendsModal)