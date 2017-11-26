import React from 'react';
import ReactDOM from 'react-dom';
import {Panel, Col} from "react-bootstrap"
//import mousetrap from "mousetrap"
import { connect } from 'react-redux';
import {authActions} from 'core/auth'

class MyProfile extends React.Component {

  constructor(props){
    super(props);
  }

  componentDidMount(){
    const {updateProfile} = this.props
    updateProfile(); //TODO: maybe no need to invoke this function
  }


  render(){

    const {
      user, 
    } = this.props;
    //console.log(user)

    const title = (
      <h3>Panel title</h3>
    );
    const panelsInstance = (
      <Col className="page" md={8} mdOffset={2}> 
        <Panel header="My Profile">
          <p><span>full name: </span> {user.user.fullname}</p>
          <p><span>email : </span> {user.user.email} </p>
          <p>id: {user.user.id}</p>
          <p>uid: {user.user.uid}</p>
          <p>createdAt: {user.user.createdAt}</p>
          <p>updatedAt: {user.user.updatedAt}</p>
        </Panel>
      </Col>
    );

    return panelsInstance 
  }
}

export default connect((state, ownProps) => ({
  user: state.auth,
}), authActions)(MyProfile);
