'use strict';
import React from 'react';
import {Button, ButtonGroup, Modal, Col, Form, FormGroup, FormControl, InputGroup, ControlLabel} from "react-bootstrap";
import {BASE_URL} from 'config';
//require('../../../assets/vender/multiselect/bootstrap-select.min.css');
//require('../../../assets/vender/multiselect/bootstrap-select.js');
var $ = require('jquery');

class RegisterMemberModal extends React.Component{
  constructor(props){
    super(props);
    this.state = {
    	useridlist:[],
    	showmemberlist: "none"
    }
  }  
  
	btnClick(){		
	  var btn = $(this);
	  const eid = this.props.eid;
	  this.hideAlertMsg();
	  //btn.button('loading');
	  var selectedUsersIDList = this.state.useridlist;
	  var that = this;
	  
	  $.post(BASE_URL + 'event/'+eid+'/addEventMemberAjax', {
	    'users': selectedUsersIDList,
	    'eid': eid
	    }).done(function(data){
	      if(data.error)
	      {
	        this.showAlertMsg(data.error);
	      }else{	
	        alert("Registration done successfully.");
	        window.location.reload();
	        return;
	      }
	    })
	    .fail(function(){
	      this.showAlertMsg();
	    })
	    .always(function(){
	      btn.button('reset');
	    })
	}
	
  hideAlertMsg(){
    if(!$('#register_event_member_alert').hasClass('hidden'))
    {
      $('#register_event_member_alert').toggleClass('hidden');
    }
  };

  showAlertMsg(message){
    if(!message)
    {
      message = 'Server or Network error.';
    }
    var dt = '<dt>'.concat(message, '</dt>');
    $('#register_event_member_alert > dl').html(dt);
    $('#register_event_member_alert').removeClass('hidden');
  };
  
  handleUserSelect = (e)=>{
    var $target = $(e.target);
    if ($target.is('li')) {
      //$('#myPillbox').pillbox('addItems', 1, [{ text: $target.html(), value: $target.attr('id'), attr: {}, data: {} }]);
      var currentValue = $('#userNameList').val().trim();  
      var id = $target.attr("id");
      //alert("id is:"+id);
      //alert(currentValue);
      if (currentValue.length==0){
        var newValue = $target.html().trim();	  
      }
      else{
        var newValue = currentValue + ";" + $target.html().trim();	
      }
      $('#userNameList').val(newValue);
      this.state.useridlist.push(id);
      this.setState({
      	showmemberlist: "block"
      })
    }
	}
  
  handleUserQuery = ()=>{
 	const groupid = this.props.groupid;
 	var username = $('#userselect').val().trim();
 	
 	if (username.length === 0){
 		$('.user-select ul').empty();
 		return;
 	}
 	
	  $.ajax({
	      url: BASE_URL + 'group/user/search',
	      data: {
	          search: username,
	          per_page: 20,
	          active: !0,
	          groupid: groupid,
	          current_user: 1
	      },
	      dataType: 'json'
	  }).done(function(data) {
	      if(data.error)
	      {
	        alert(data.error);
	      }else{
	        $('.user-select').css('display','none');
	        $('.user-select ul').empty();
	        $('.user-select').css('display','block');	        
	        for(var i=0; i<data.user.length; i++){
	          $('.user-select ul').append('<li id='+data.user[i].id+' >'+data.user[i].fullname+'</li>');  
	        }
	        $('.user-select ul li').css('display','inline-block');
	        $('.user-select ul li').css('float','left');
	        $('.user-select ul li').css('padding','8px 20px');
	        $('.user-select ul li').css('line-height','20px');	        
	      }
	  });
  }	
  
  enterModal = ()=>{
  	if (this.state.showmemberlist!="none"){
  		this.setState({
  			showmemberlist:"none" //if the modal is activated again after hide it, showmemberlist need to be set to default "none" value
  		})
  	}
  }
	
	render(){
		//console.log("aaa:"+this.state.showModal);
		return (			
			<Modal show = {this.props.showModal} onHide={this.props.closeModal} onEnter={this.enterModal} bsSize="lg">			
				<Modal.Header closeButton>
				  <Modal.Title>Register members to event</Modal.Title>				
				</Modal.Header>
				<Modal.Body>
				  <Form horizontal>		
				    <FormGroup>
				      <Col sm={12}>
			          <div id="register_event_member_alert" className="alert alert-danger hidden" role="alert">
			            <dl>
			            </dl>
			          </div>	
						    <div style={{paddingTop: "6px", paddingRight: "12px", paddingBottom: "6px", paddingLeft: "12px", display:this.state.showmemberlist}}>
							    <FormGroup controlId="userNameList" >
							      <ControlLabel>Members List</ControlLabel>
							      <FormControl componentClass="textarea" placeholder="" />
							    </FormGroup>
						    </div>
				      </Col>
				    </FormGroup>					    				   
				    <FormGroup>	
				      <Col sm={12}>
					      <div className="input-group">
			            <span className="input-group-addon" id="basic-addon1">Search by</span>
			            <input type="text" id="userselect" className="form-control" onKeyUp={this.handleUserQuery} placeholder="Username" aria-describedby="basic-addon1" />
			          </div>			
			          <div className="user-select" style={{display:"none", paddingLeft:"60px"}}>
			            <ul className="user-for-select" onClick = {this.handleUserSelect}></ul>
			          </div>
              </Col>
				    </FormGroup>													    				   
				  </Form>			
				</Modal.Body>
    		<Modal.Footer>
	        <Button type="submit" onClick = {this.btnClick.bind(this)}>
	          Save
	        </Button>
	        <Button type="button" onClick = {this.props.closeModal}>
	          Close
	        </Button>		          
    		</Modal.Footer>				
			</Modal>
  	)		
	}
	
}

export default RegisterMemberModal;