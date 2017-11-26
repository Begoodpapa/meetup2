import React from 'react';
import { connect } from 'react-redux';
import {Panel, Col} from "react-bootstrap";
import {BASE_URL} from 'config';
var $ = require('jquery');

class MyGroup extends React.Component {	
  constructor(props){
  	super(props);
  		
  	this.state={
  		groupsarray:[],
  		authenticated: this.props.auth.authenticated
  	};
  }
  
  componentDidMount(){
  	this.getmygroup();
  }

  componentWillReceiveProps(nextProps){
  	if ((nextProps.auth.authenticated) && (!this.state.authenticated)){
  		this.setState({
  			authenticated: true
  		}, ()=>{
  			this.getmygroup();
  		})
  	}
  }
  
  getmygroup(){
    const {
      auth
    } = this.props;    

    if ((!auth.authenticated) && (!this.state.authenticated)) return;
    
    let url = BASE_URL + 'user/showMyGroupAjax';
    const that = this;    
    
    $.get(url, function(data, result){
    	if (data.error){
    		let content = (
    			<div><h4>Get My Group Error!</h4></div>
    		);
    		that.setState({
    			groupsarray: content
    		});    		
    	}
    	else if (data.groups.length === 0){
    		let content = (
    			<div><h4>You have never enrolled any group!</h4></div>
    		);    
    		that.setState({ 
    			groupsarray: content
    		});       		
    	}else{
    		//console.log("length is"+data.groups.length);    
    		let groupsarray = data.groups.map(function(group){    			
    			//console.log("group.id:"+group.id);
    			let href = '#/group/show/' + group.id + '/overview';
	    		let groupfd = (group.groupfd)?(BASE_URL + (group.groupfd)):(BASE_URL + '/images/group_default.jpg');
	    		let groupname = (group.name)?(group.name):'';
	    		let usernum = (group.user)?(group.user.length):'0';    			
    			return(
						<Col sm={6} md={4} key={group.id}> 
				  		<div className="thumbnail" style={{minHeight:"430px"}}>
				  			<a href = {href} >									  			
					  			<h4> {groupname} </h4>
					  			<img style={{width:'100%', Height:'300px'}} src= {groupfd} />							  			  
					  			<p> {usernum} members</p>
				  			</a>
				  		</div> 
				  	</Col>       				  						  													
    			)
    		}); 
    		that.setState({ 
    			groupsarray: groupsarray
    		});
    	}
    })
  }

  render(){

    const {
      auth
    } = this.props;
    //console.log("length is:"+this.state.groupsarray.length);

    let count = this.state.groupsarray.length;
    count = (count>0)?'(' + count + ')': '';
    
    let head = "My Group" + count;
    
    let note = (<div></div>);
    if (!auth.authenticated){
    	note = (<div><h4> You are not authenticated for this query. Please log in. </h4></div>)
    }
            
    return (
      <Col md={12} style={{paddingTop:'80px'}}> 
        <Panel header={head}>                  
					<div className="container">
					    <div className="row" id = "row-content">					      
					      {this.state.groupsarray}  
					      {note}
					    </div>
					</div>         
        </Panel>
      </Col>
    )
  }
}

export default connect((state, ownProps) => ({
  auth: state.auth,
}))(MyGroup);
