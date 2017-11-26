import { connect } from 'react-redux'; 
import React from 'react'; 
import {Grid, Row, Col, Modal} from "react-bootstrap";
require('../../../assets/styles/homePage.css');
import JoinUsModal from "components/footer/joinusmodal";
//require('../../../assets/vender/bootstrap/dist/css/bootstrap.min.css');
//require('../../../assets/vender/bootstrap/dist/css/bootstrap-theme.min.css');
//require('../../../assets/styles/animate.css');


class Footer extends React.Component {

	constructor(){
		super();
		
		this.state = {
			showmodal : false
		}
	}

	showmodal(){
		this.setState({
			showmodal : true
		});
	}
	
	closemodal = ()=>{
		
		this.setState({
			showmodal : false
		});		
	}
  
  render(){
    
    return (
	   <footer >
	      <div className="container">
	        <div className="row">
	          <div className="col-sm-6">
	            <h2>Useful links for you</h2>
	            <ul className="links">
	              <li><a href="/aboutus" >About us</a></li>
	              <li><a data-toggle="modal" onClick= {this.showmodal.bind(this)} >Join us</a></li>
	              <li><a href="http://hzegsav40.china.nsn-net.net:4567/" >Discuss</a></li>
	              <li><a href="/thanks">Contribution</a></li>
	              <JoinUsModal
	                showmodal = {this.state.showmodal}
	                closemodal = {this.closemodal}
	              />
	            </ul>
	          </div>
	          <div className="col-sm-6 message">
	            <h3>Beehive</h3>
	            <p>This site was crafted with Nokia Ranking System Development Group and implemented by hand using <a href="http://www.sailsjs.org/" title="Sails Js" target="_blank">Sails</a> (build base on the most popular web server <a href="https://nodejs.org/" title="Nodejs" target="_blank">Nodejs</a>). The site is fully responsive and will adapt to the device you are viewing it on as we using the responsive front-end framework-<a href="http://bootstrap.evget.com/" title="Boostrap" target="_blank">Bootstrap</a>. </p>
	            <p>Special thanks to all team members for your contribution that making great design and user experiences.</p>
	          </div>
	        </div>
	        <div className="row small">
	          <div className="col-sm-12">
	            <small>Copyright © 2017, Nokia</small>
	          </div>
	        </div>
	      </div>
	    </footer>
    )
  }
}

export default Footer
