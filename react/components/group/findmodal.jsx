'use strict'; 
import React from 'react';
import {Modal, Form, FormGroup, FormControl, Button, ControlLabel, Col} from "react-bootstrap";

class FindModal extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      name: '',
      id: ''
    };
  }

  changeName(e){
  	
  	var idValue=document.getElementById("groupid").value.trim();  	
  	
    this.setState({name: e.target.value})
    
  	if (idValue.length == 0) {
      this.setState({id: '0'}); //zero means empty input of id, because Database starts from 1 for id number.
      //console.log("empty idValue");
    }else{
   	  this.setState({id: idValue});
    }    
  }
  
  changeId(e){
  	var nameValue=document.getElementById("groupname").value.trim();  	
  	//console.log("groupname is:"+nameValue);

  	if (e.target.value.trim() == ''){
      this.setState({id: '0'}) //zero means empty input of id, because Database starts from 1 for id number.
      //console.log("empty idValue");
    }else{
   	  this.setState({id: e.target.value});
    }
    
    this.setState({name: nameValue});
  }
  
  setdefault(){
    this.setState({id: '', name: ''});
  }
  
  render(){
		return (			
			<Modal show = {this.props.showmodal} onHide={this.props.closemodal} bsSize="lg">			
				<Modal.Header closeButton>
				  <Modal.Title>Find Group</Modal.Title>				
				</Modal.Header>
				<Modal.Body>
				  <Form horizontal>				    
				    <FormGroup controlId="groupname">
				      <Col componentClass={ControlLabel} sm={3} >
				        Group name contains
				      </Col>
				      <Col sm={7}>
				        <FormControl type="text" onChange={this.changeName.bind(this)} />
				      </Col>
				    </FormGroup>
				
				    <FormGroup controlId="groupid">
				      <Col componentClass={ControlLabel} sm={3}>
				        or ID is
				      </Col>
				      <Col sm={7}>
				        <FormControl type="text" onChange={this.changeId.bind(this)} />
				      </Col>
				    </FormGroup>		    				    
				  </Form>			
				</Modal.Body>
				<Modal.Footer>
	        <Button type="submit" href = {"#groupsr/" + this.state.id + "/" + this.state.name} onClick = {this.props.closemodal}>
	          Submit
	        </Button>
	        <Button type="button" onClick = {this.props.closemodal}>
	          Close
	        </Button>				
				</Modal.Footer>				
			</Modal>
  	)
	}
}

export default FindModal;
