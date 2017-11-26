'use strict';
import React from 'react';
import {Button, Modal} from "react-bootstrap";
import {BASE_URL} from 'config';
var $ = require('jquery');

class EventPublishModal extends React.Component{
	constructor(props){
		super(props);		
	}
	
	/*
	componentWillReceiveProps(nextProps){
		if ((nextProps.showModal) && (!this.state.showModal)){
			this.setState({
				showpublish: true
			})
		}
	}
	*/
		
  publishEvent(gid, eid){
  	var url = BASE_URL + "group/" + gid + "/event/" + eid + "/publish";
  	
  	/*
    this.setState({
		  showmodal: false    	
    });
    */
   
   this.props.closeModal();
			    
		$.get(url,{
      gid: gid,
      eid: eid
    })
      .done(function(data){
        if(data.error){
          $('#errMsgLabel').text(data.error);
          $('#errMsgDiv').show();
        }else{        	       
					alert("Operation Succeeded.");						
					//location.href = '#/group/show/'+gid+'/eventshow/'+ eid;					 
					location.reload();
				}							
			})
      .fail(function(xhr, status, errorThrown){
        console.log(status + errorThrown);
        $('#errMsgLabel').text(status );
        $('#errMsgDiv').text(errorThrown);
        $('#errMsgLabel').show();
        $('#errMsgDiv').show();
      });  	
  }
		
  render(){  	
		const{
		  groupid,
		  eid
		} = this.props;

  	return(
  		
		  <Modal bsSize="small" show = {this.props.showModal} onHide={this.props.closeModal}>
        <Modal.Header closeButton>          
          <Modal.Title>Notice</Modal.Title>
        </Modal.Header>
				<Modal.Body>
           <p>The event invitation will be sent to all the group members by email, are you sure ?</p>
        </Modal.Body>
    		<Modal.Footer>
          <Button onClick={this.props.closeModal}>Close</Button>
          <Button id="publish" onClick={this.publishEvent.bind(this, groupid, eid)}>Yes, I'm sure!</Button>          
    		</Modal.Footer>
		  </Modal>	  
  		
    )}
}

export default EventPublishModal;