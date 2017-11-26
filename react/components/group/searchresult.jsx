'use strict'; 
import React from 'react';
import {connect} from 'react-redux'; 
import GroupArr from 'components/group/grouparray';
import {Col, Panel} from 'react-bootstrap';

class GroupSR extends React.Component {	
	render(){
		const{
			params
		} = this.props;
		
		//console.log("GroupSR....groupId"+params.groupId);
		//console.log("GroupSR....groupName"+params.groupName);
    
    let head = "Search Result of: Group Name Contains [" + params.groupName + "] Or Group ID is [" + params.groupId + "]";

		return (
			
      <Col md={12} style={{paddingTop:'80px'}}> 
        <Panel header={head}>                  
					<div className="container">
				    <div className="row" id = "row-content">					      
					    <GroupArr
					      searchid = {params.groupId}
					      searchstr = {params.groupName}
					      type = 'search'
					    />		
				    </div>
					</div>         
        </Panel>
      </Col>			

		)
	}
}

export default GroupSR