'use strict'; 
import React from 'react';
import {Modal} from "react-bootstrap";

class JoinUsModal extends React.Component {
	
	render(){
		return (			
			<Modal show = {this.props.showmodal} onHide={this.props.closemodal}>			
				<Modal.Header closeButton>
				  <Modal.Title>Welcome to join us</Modal.Title>				
				</Modal.Header>
				<Modal.Body>
					<p>If you're interested in Beehive and Node.js development, and are willing to learn new things, don't hestitate to join us - just send an email to <a href="mailto:gang-layner.wang@nokia.com?subject=I'd like to join Beehive development">Wang, Gang-Layner</a>.</p>
	        <p>We have Javascript/Node.js trainings and pair work sessions to ramp you up on Beehive development.</p>				
				</Modal.Body>
				<Modal.Footer>
					<button type="button" className="btn btn-default" onClick={this.props.closemodal}>OK</button>
				</Modal.Footer>
			</Modal>
  	)
	}
}

export default JoinUsModal;