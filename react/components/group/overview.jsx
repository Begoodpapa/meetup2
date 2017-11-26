'use strict'; 
import React from 'react';
import {Tabs, Tab} from "react-bootstrap";
import ComingEvents from 'components/event/comingevents';
import PastEvents from 'components/event/pastevents';
import FullCalendar from 'components/group/fullcalendar';

class GroupOverview extends React.Component {
  
  showgroupdesc(){
  	if (this.props.groupdesc){
      return {__html: this.props.groupdesc};
    }else{
    	return {__html: ""};
    }
  }

  showeventdesc(){  	
    if (this.props.RecentEvent.desc){
      return {__html: this.props.RecentEvent.desc};	
    }else{
    	return {__html: ""};	
    }  	      	
  }
  
  getrecentevent(){
  	let b_date, b_time, e_date, e_time = '';  	  	
  	
  	if (this.props.RecentEvent.topic){
  	  let begindate = new Date(this.props.RecentEvent.begindate);	
  	  b_date = 'Begin:' + begindate.toLocaleDateString();
  	  b_time = begindate.toLocaleTimeString();  	  
  	}
  	
  	if (this.props.RecentEvent.topic){
  	  let enddate = new Date(this.props.RecentEvent.enddate);	
  	  e_date = 'End:' + enddate.toLocaleDateString();
  	  e_time = enddate.toLocaleTimeString();  	   		
  	}
  	  	
  	return(
				<div id="recent-event" className ="tab-pane group-event-tab active">
         	<div id="event_title">
    			{/*<h2 style="margin-top:5px"> <a href="#<%= '/group/'.concat(group.id, '/event/', RecentEvent.id, '/show') %>"><%= RecentEvent.topic %>RecentEvent.topic</a></h2>*/}
						<h2 style={{marginTop:'5px'}}> {this.props.RecentEvent.topic?this.props.RecentEvent.topic:'No Recent Topic'}</h2>
    		  </div>
    			<div id="event-content">
    				<div id="event_when">
              <time itemProp="startDate" dateTime="2015-03-14T09:30:00+08:00">
              	<h4 className="h4-date"> {b_date}</h4>
                <p className="subtext"> {b_time} </p>		     
                <h4 className="h4-date"> {e_date} </h4>
                <p className="subtext">{e_time}</p>	               
              </time>
            </div>
            <div id="event_where">
              <h3>{this.props.RecentEvent.address?this.props.RecentEvent.address:''}</h3>
            </div>

            <div id="divide-line">
            </div>
            
            <div className="event-desc">		           
              <div dangerouslySetInnerHTML={this.showeventdesc()}></div>
            </div>
          </div>
	      </div>
    )
  }
  
  getcomingevents(){
  	return(
  		<ComingEvents
	      comingEvents = {this.props.comingEvents}
	      groupid = {this.props.groupid}
	    />
  	)
  }
  
  getpastevents(){
  	return(
  		<PastEvents
	      pastEvents = {this.props.pastEvents}
	      groupid = {this.props.groupid}
	    />
  	)
  }  
  
  getfullcalendar(){
  	return(
  		<FullCalendar
	      events = {this.props.events}
	      groupid = {this.props.groupid}
	    />
  	)
  }    

  render(){
  	const{
  		groupdesc,
      pastEvents,
      comingEvents,
      RecentEvent,
      groupid
  	} = this.props;
  	
  	//console.log("recentevent topic is:"+this.props.RecentEvent.topic);
  	
  	let b_date, b_time, e_date, e_time = '';  	  	
  	
  	if (this.props.RecentEvent){
  	  let begindate = new Date(this.props.RecentEvent.begindate);	
  	  b_date = 'Begin:' + begindate.toLocaleDateString();
  	  b_time = begindate.toLocaleTimeString();  	  
  	}
  	
  	if (this.props.RecentEvent){
  	  let enddate = new Date(this.props.RecentEvent.enddate);	
  	  e_date = 'End:' + enddate.toLocaleDateString();
  	  e_time = enddate.toLocaleTimeString();  	   		
  	}
  	
  	return(
    <div>		
      <div className="panel panel-default">
	      <div className="panel-body">
			    <div className="group-desc-div">
            <div id="groupdesc" dangerouslySetInnerHTML={this.showgroupdesc()}></div>
	        </div>
	      </div>
	    </div>
	    <div className="panel panel-default">
	      <div className="panel-heading">
	        <h1 id="welcome-msg" className="panel-title">Welcome!</h1>
	      </div>	      
	      <Tabs defaultActiveKey={1} id="tabs">
		      <Tab eventKey={1} title="Recent Event">{this.getrecentevent()}</Tab>
		      <Tab eventKey={2} title="Coming Events">{this.getcomingevents()}</Tab>
		      <Tab eventKey={3} title="Past Events">{this.getpastevents()}</Tab>
		      <Tab eventKey={4} title="Calendar">{this.getfullcalendar()}</Tab>
	      </Tabs>	  
	    </div>	      	   
	  </div>  
  )
 	//this.showgroupdesc();
  }
}

export default GroupOverview;

/*
export default connect((state, ownProps) => ({
  hash: state.routing.locationBeforeTransitions.hash, 
  allgroups: state.group.allGroups,
  auth: state.auth
}), groupActions )(Groupsidebar);
*/