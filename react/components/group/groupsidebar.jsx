'use strict'; 
import { connect } from 'react-redux';
import React from 'react'; 
import {BASE_URL} from 'config';


class Groupsidebar extends React.Component {

  show_editgroup_btn(){  	
  	const{
  	  auth,
  	  ownerid,
  	  groupid
    } = this.props;

    //console.log("ownerid is:"+ownerid);	
      
		if ((auth.authenticated) && ( auth.user.id===ownerid)){
      //console.log("auth.user.id is:"+auth.user.id);			
			var hlink = "#/group/manage/edit/" + groupid;
		  return(
		    <div id="groupEditDiv"><a role="button" className="btn btn-default" href={hlink}>Edit Group</a></div>
		    )
		}
		else{
			return (
				<div id="groupEditDiv"></div>
			)
		}
  }

  render(){
  	
  	const {
      groupname,
      groupowner_fullname,
      groupowner_email,
      groupfd,
      num_members,
      pastEvents,
      comingEvents,
      events,
      userfd,
      groupid
    } = this.props;
  	
    var userimgurl = (!this.props.userfd) ? (BASE_URL + '/images/default_upp.jpg') : (BASE_URL + userfd);  	
    var groupimgurl = (!this.props.groupfd) ? (BASE_URL + '/images/group_default.jpg') : (BASE_URL + groupfd);

	  //console.log("groupname is: "+groupname);
    //console.log("num_members is: "+num_members);	 
    var p_events_num = this.props.pastEvents.length;
    var c_events_num = this.props.comingEvents.length;
    var events_num = this.props.events.length;
    
    var membershref = '#/group/show/' + groupid + '/member';
    var p_eventshref = '#/group/show/' + groupid + '/pastevent';
    var c_eventshref = '#/group/show/' + groupid + '/comingevent';
    var calendarhref = '#/group/show/' + groupid + '/calendar';
    var emailhref = 'mailto:' + groupowner_email + '?Subject=Hello';
      
    //console.log("this.props.pastEvents:"+this.props.pastEvents.length);    

    return (    	    
    	
		<div className="row">
		  <div className="col-md-12">
		    <div className="panel panel-default">
		      <div className="panel-body" style={{width:'100%',height:'270px'}}>
		        {/*-- groupCarousel --*/}
		        <div id="groupCarousel" className="carousel slide" data-ride="carousel" data-interval="5000">
		          <div className="carousel-inner" role="listbox">
		            <div className="item active">           
		             <img src={groupimgurl} alt={groupfd} />
		            </div>
		          </div>
		        </div>
		        {/*-- end groupCarousel --*/}
		      </div>
		      <ul className="list-group">
		        <li className="list-group-item">
		          <p className="lead truncate-text">{groupname}</p>
		          <ul className="list-group">         
		            <a href={membershref}>
		              <li className="list-group-item">
		               <span className="badge">{num_members}</span>
		                Members
		              </li>
		            </a>        
		            <a href={p_eventshref}>
		              <li id="pastEventLi" className="list-group-item">               
		                <span className="badge">{p_events_num}</span>
		                Past Event
		              </li>
		            </a>            
		            <a href={c_eventshref}>
		              <li id="comingEventLi" className="list-group-item">               
		                <span className="badge">{c_events_num}</span>                
		                Coming Event
		              </li>
		            </a>            
		            <a href={calendarhref}>
		              <li id="groupCalendarLi" className="list-group-item">             
		               <span className="badge">{events_num}</span>     
		                Calendar
		              </li>
		            </a>
		          </ul>
		        </li>
		        <li className="list-group-item">
		          <h4>Organizer: </h4>
		          <div className="thumbnail">
		
		            <img src= {userimgurl} alt="Picture of Organizer" />
		
		            <div className="caption">             
		             	<h5>{groupowner_fullname}</h5>
		            </div>
		            <button type="button" className="btn btn-default btn-block" aria-label="Contact" >
		             {/*<a href="mailto:<%= group.owner.email%>?Subject=Hello" target="_top">*/}
		              <a href={emailhref} target="_top">
		              <span className="glyphicon glyphicon-envelope" aria-hidden="true"></span> Contact</a>
		            </button>
		          </div>
		        </li>
		        <li className="list-group-item">
		          <h5 className="truncate-text">We're about: {/*<%= group.tags ? group.tags : "..." %>*/} </h5>
		        </li>
		        <li className="list-group-item">
		          {this.show_editgroup_btn()}
		        </li>
		      </ul>
		    </div>
		  </div>
		</div>
    	    	    
  )}
}

//export default Groupsidebar;

export default connect((state, ownProps) => ({
  allgroups: state.group.allGroups,
  auth: state.auth
}))(Groupsidebar);
