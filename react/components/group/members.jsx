'use strict'; 
import React from 'react';
import { connect } from 'react-redux';
import {table} from "react-bootstrap";

class GroupMembers extends React.Component {
  
  render(){
  	const{
			allgroups,
      groupid
  	} = this.props;

  	
  	var groupmembers = [];
  	
  	allgroups.map(function(group){
  		//console.log("groupid is:"+group.id);
  		if (group.id == groupid){
  	    groupmembers = group.user.map(function(user){
  	    //console.log("user.id is:"+user.id);
  	    //console.log("user.id fullname:"+user.fullname);	  	    
  	      return (
  	      	<tr key={user.id}>
    					<td>{user.id}</td>
    					<td>{user.fullname}</td>
    					<td>{user.email}</td>
  					</tr>
  	      )
  	    })
  		}  		  
  	})
  	
  	//console.log("length of groupmembers is:" + groupmembers.length);
	
  	return(
			<table className = "table">
			  <thead>
			    <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
          </tr>
        </thead>  
        <tbody> 
			    {groupmembers}
			  </tbody>
			</table>
  )}
}

export default connect((state, ownProps) => ({ 
  allgroups: state.group.allGroups
}) )(GroupMembers);
