'use strict';
import React from 'react';
import { connect } from 'react-redux';
import {Panel, Row, Col, ListGroup, ListGroupItem} from "react-bootstrap";
import {BASE_URL} from 'config';
var $ = require('jquery');

class MyEvent extends React.Component {	
  constructor(props){
  	super(props);
  		
  	this.state={
  		eventsarray:[],
  		authenticated: this.props.auth.authenticated
  	};
  }
  
  componentDidMount(){
  	this.getmyevent();
  }

  componentWillReceiveProps(nextProps){
  	if ((nextProps.auth.authenticated) && (!this.state.authenticated)){
  		this.setState({
  			authenticated: true
  		}, ()=>{
  			this.getmyevent();
  		})
  	}
  }
  
  getmyevent(){
    const {
      auth
    } = this.props;    

    if ((!auth.authenticated) && (!this.state.authenticated)) return;
  
    let url = BASE_URL + 'user/showMyEventAjax';
    const that = this;    
    
    $.get(url, function(data, result){
    	if (data.error){
    		let content = (
    			<div><h4>Get My Event Error!</h4></div>
    		);
    		
    		that.setState({ 
    			eventsarray: content
    		});    	
    	}
    	else if (data.events.length === 0){
    		let content = (
    			<div><h4>You have never participated in any event!</h4></div>
    		);    
    		
    		that.setState({ 
    			eventsarray: content
    		});       		
    	}else{
    		//console.log("length is"+data.events.length);    
    		let eventsarray = data.events.map(function(event){
    			
    			//console.log("event.id:"+event.id);
    			let href = '#/event/show/' + event.id + '/overview';	    		
	    		let eventtopic = (event.topic)?(event.topic):'';
	    		let eventadd = (event.address)?(event.address):'';
	    		let usernum = (event.user)?(event.user.length):'0';   
	    		
					let begindate = new Date(event.begindate);
					let b_date = begindate.toLocaleDateString();
					let hours = begindate.getHours();
					if (hours<10) {
						hours = '0' + hours;
					}
					let minutes = begindate.getMinutes();
					if (minutes<10) {
						minutes = '0' + minutes;
					}			
					
					let fulltime = hours + ':' + minutes;	    		
	    			    		    	
    			return(    				
	          <Row key={event.id} style={{marginBottom: "10px"}}>
	            <Col xs={3} sm={3} md={3} lg={3}>         
	              <h5> {b_date} </h5>
	              <h5> {fulltime} </h5>
	            </Col>
	            <Col xs={9} sm={9} md={9} lg={9}>
	              <div> {eventadd} </div>
	              <div>
	                <a href= {href} > {eventtopic} </a>
	              </div>
	              <div>
	              	{usernum} <span>hacks Going</span>
	              </div>
	            </Col>	         
	          </Row>    				    				  						  											
    			)  
    		});    		
    		that.setState({ 
    			eventsarray: eventsarray
    		});    		
    	}
    })
  }

  render(){

    const {
      auth
    } = this.props;
    //console.log("length is:"+this.state.eventsarray.length);

    let count = this.state.eventsarray.length;
    count = (count>0)?'(' + count + ')': '';
    
    let head = "My Event" + count;
    
    let note = (<div></div>);
    if (!auth.authenticated){
    	note = (<div><h4> You are not authenticated for this query. Please log in. </h4></div>)
    }
            
    return (
      <Col md={8} mdOffset={2} style={{paddingTop:'80px'}}> 
        <Panel header={head}>                  
					<div className="container">					    		
			      {this.state.eventsarray}
			      {note}
					</div>         
        </Panel>
      </Col>
    )
  }
}

export default connect((state, ownProps) => ({
  auth: state.auth,
}))(MyEvent);
