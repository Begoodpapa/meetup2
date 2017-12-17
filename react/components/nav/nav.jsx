import { connect } from 'react-redux';
import React, { Component, PropTypes } from 'react';
import { Navbar, NavItem, Nav, NavDropdown, MenuItem } from 'react-bootstrap';
import { authActions } from 'core/auth';
import { loginmodalActions } from 'core/loginmodal';
import LoginModal from "components/auth/login";
import FindModal from "components/group/findmodal";

class UserNavItem extends React.Component {

  render() {
    const {
      auth,
      login,
      logout,
      openLoginModal,
      service,
      request,
      bottle
    } = this.props

    if(!auth.authenticated) {
      return(
        <Nav pullRight>
          <NavItem eventKey={1} href="#" onClick={openLoginModal.bind(this)}> Log in </NavItem>
          <LoginModal />
        </Nav>
      )
    } else {

      return(
        <Nav pullRight>
          <NavDropdown eventKey={1} title={auth.user.fullname} id="basic-nav-dropdown">
            <MenuItem href="#myprofile" eventKey={1.1}>My profile</MenuItem>
            <MenuItem href="#mygroup" eventKey={1.2}>My Group</MenuItem>
            <MenuItem href="#myevent" eventKey={1.3}>My Event</MenuItem>
            <MenuItem divider />
            <MenuItem eventKey={1.3} onClick={logout.bind(this)}>Log out</MenuItem>
          </NavDropdown>
        </Nav>
      )
    }
  }
}

class NavApp extends React.Component {
  constructor() {
    super();

    this.state = {
      showgrpfind: false
    }
  }

  showgrpfind() {
    this.setState({
      showgrpfind: true
    })
  }

  closegrpfind = () => {
    this.setState({
      showgrpfind: false
    })
  }

  static propTypes = {
    login: PropTypes.func.isRequired,

  };

  render() {
    const {
      auth,
      login,
      logout,
      openLoginModal,
      bottle,
      service,
      request
    } = this.props

    var style = { color: "#00d8ff" }

    const navbarInstance = (
      <Navbar inverse fixedTop style={{"backgroundColor":"#181718"}}>
        <Navbar.Header>
          <Navbar.Brand>
            <a href="/" style={style}>Beehive</a>
          </Navbar.Brand>
          <Navbar.Toggle />
        </Navbar.Header>
        <Navbar.Collapse>
          <Nav>
            <NavItem eventKey={1} href="#group/manage/new">New</NavItem>
            <NavItem eventKey={2} onClick={this.showgrpfind.bind(this)}>Find</NavItem>
            <FindModal 
              showmodal = {this.state.showgrpfind}
              closemodal = {this.closegrpfind}
            />
            <NavItem eventKey={3} href="http://beehive.eecloud.dynamic.nsn-net.net:1338">Persona</NavItem>
            <NavItem eventKey={4} href="http://beehive.eecloud.dynamic.nsn-net.net:1341">Webond</NavItem>
            <NavItem eventKey={5} href="http://beehive.eecloud.dynamic.nsn-net.net:4567">Discuss</NavItem>
          </Nav>
          <UserNavItem 
            auth={auth} 
            login={login} 
            logout={logout} 
            openLoginModal={openLoginModal}
            service={service}
            request={request}
            bottle={bottle}
            />
        </Navbar.Collapse>
      </Navbar>
    );

    return navbarInstance
  }
}

export default connect((state, ownProps) => ({
  auth: state.auth
}), Object.assign({}, authActions, loginmodalActions))(NavApp);