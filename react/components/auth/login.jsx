import React from 'react';
import ReactDOM from 'react-dom';
import {Input, Panel, Modal, Col, InputGroup, FormControl, ControlLabel, Form, FormGroup, Checkbox, Button} from "react-bootstrap"
import { authActions } from 'core/auth';
import { loginmodalActions } from 'core/loginmodal';
import { connect } from 'react-redux';

class LoginModal extends React.Component {

  constructor(props){
    super(props);
    this.state = {
      name: '',
      passwd: ''
    };
  }

  changeName(e){
    this.setState({name: e.target.value})
  }
  changePasswd(e){
    this.setState({passwd: e.target.value})
  }

  render(){

    const{loginmodal, login, closeLoginModal} = this.props
    const doLogin=()=>{
      login(this.state)
      closeLoginModal()
    }

    return (
      <Modal bsSize="small" show={loginmodal.showLoginModal} onHide={closeLoginModal.bind(this)}>
        <Modal.Header closeButton >
          <Modal.Title>Login to Beehive</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <ControlLabel>Username:</ControlLabel>
          <FormControl type="email" placeholder="userid" onChange={this.changeName.bind(this)}/>

          <ControlLabel>Passwd:</ControlLabel>
          <FormControl type="password" placeholder="password" onChange={this.changePasswd.bind(this)}/>

          <Checkbox>Remember me</Checkbox>

        </Modal.Body>
        <Modal.Footer>
          <Button onClick={doLogin.bind(this)}>login </Button>
        </Modal.Footer>
      </Modal>
    )
  }
}

export default connect((state, ownProps) => ({
  loginmodal: state.loginmodal,
}), Object.assign({}, authActions, loginmodalActions ))(LoginModal);


