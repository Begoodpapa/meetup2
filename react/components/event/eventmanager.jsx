'use strict';
import React from 'react'; 
import {connect} from 'react-redux';
import {BASE_URL} from 'config';
import SimditorTextarea from 'components/simditor';
require('../../../assets/js/bootstrap-datetimepicker-master/css/bootstrap-datetimepicker.css');
require('../../../assets/js/bootstrap-datetimepicker-master/js/bootstrap-datetimepicker.js');
var $ = require('jquery');
var Common = require('../../common.js');

class EventMgr extends React.Component{ 
	constructor(props){
		super(props);
		
		this.state ={
			targetevent: {},
			attached_tags_json: []
		}
	}
	
	defaultTime(){
	  const{
	    action
	  } = this.props;	 
	  
	  if (action === 'add'){
	    var nowDate = new Date();
	    
	    var year = nowDate.getFullYear().toString();
	    var month = (nowDate.getMonth()+1)>9 ? (nowDate.getMonth()+1).toString() : '0' + (nowDate.getMonth()+1);
	    var day = nowDate.getDate()>9 ? nowDate.getDate().toString() : '0'+nowDate.getDate();
	    
	    var date = year + '-' + month + '-' + day; 	    
      
      return (date + " " + nowDate.getHours()+':'+'30');
    }
	}	
	
	getevent(gid, eid){
			 
	  var eventid = (eid>0)? eid : 0;
	  var groupid = (gid>0)? gid : 0;	  
	  
	  //console.log("target event id is:"+groupid);		  
	   
		var url = BASE_URL + 'group/' + groupid + '/event/' + eventid + '/show';
		var that = this;
		
		$.get(url, function(data, result){			
			if (data.error){
				//console.log("error received");
				$('#event-details').html('<h3>no event is found</h3>');
			}
			that.setState({
				targetevent: data.event
			})
		});			  
	}
		
	
	componentDidMount(){
		$('#inputBeginTime').datetimepicker({
      format: "yyyy-mm-dd hh:ii",
      autoclose: true,
      todayBtn: true,
      pickerPosition: "bottom-left"
    });  

		$('#inputEndTime').datetimepicker({
      format: "yyyy-mm-dd hh:ii",
      autoclose: true,
      todayBtn: true,
      pickerPosition: "bottom-left"
    }); 
    
	  if ((this.props.action === 'edit') && (!this.state.targetevent.id)){ 
      this.getevent(this.props.groupid, this.props.eid);  
	  }		  
	}
		
	componentWillReceiveProps(nextProps){			
		if ((nextProps.action === 'edit') && (this.state.targetevent.id) && (nextProps.eid!=this.props.eid)){ //edit another event
		  console.log("event id changed");	
		  this.getevent(nextProps.groupid, nextProps.eid);
		}			
		
	}
		
	
	handleInputChange = (e)=>{		
		if (e.target.id === "inputAddress"){
			//alert('inputAddress');
	    var event = Object.assign({}, this.state.targetevent, {address: e.target.value});
			this.setState({targetevent: event});
		}else if (e.target.id === "inputTopic"){
			//alert('inputTopic');
	    var event = Object.assign({}, this.state.targetevent, {topic: e.target.value});
			this.setState({targetevent: event});
		}
	}	

	loadDesc(){
		const{	  
	    action	    
	  } = this.props;	  
	  
	  if ((action === 'edit') && (this.state.targetevent.id)){ //redux store parameters are ready
	  
	    return(
        <SimditorTextarea
          id='rteditor'
          value = {this.state.targetevent.desc}  
          onChange = {this.updateEditContent}          
        />	 
      )  
	  }
	  else if ((action === 'edit') && (!this.state.targetevent.id)){ //redux store parameters are not ready, or it store parameters are ready but desired group info haven't been parsed
	  
	  	return(
        <div> <h4>Loading...</h4></div>
			)
	  } 	  
	  else if (action === 'add'){	  	
	  	return (
        <SimditorTextarea
          id='rteditor'
          value = ''       
          onChange = {this.updateEditContent}
        />
			)	  
	  } 
	}

	updateEditContent = (value)=>{
		document.getElementById("hiddeneditor").innerHtml =value;
	}
	
	handleTimeChange = (e)=>{
		//console.log("newDate", newDate.getHours());
		var b_time = $("#inputBeginTime").val();
		
		alert("b_time is:" + b_time);
		
		var e_time = $("#inputEndTime").val();
		
		alert("e_time is:" + e_time);		
	}
	
  saveEvent(is_need_publish) {  	 
    var bgtime = $('#inputBeginTime').val();
    var datetimeobj = Common.parseDateTime(bgtime);
    var beginDate = datetimeobj.datestr;
    var beginTime = datetimeobj.timestr;
    
    var totime = $('#inputEndTime').val();
    var datetimeobj = Common.parseDateTime(totime);
    var endDate = datetimeobj.datestr;
    var endTime = datetimeobj.timestr;    
    
    var topic = $('#inputTopic').val();
    var groupid = $('#groupid').val();
    var address = $('#inputAddress').val();
     
		if (!this.props.auth.authenticated){
			alert("You need to sign in before submitting the data");
			return false;
		}    
    
    //TODO: validate date and time

    var eventDetail = document.getElementById("hiddeneditor").innerHtml;	    
    //alert(eventDetail);
    var tagList = [];
    
    {/*TODO parse tags
    var addedTags = $('#myPillbox').pillbox('items');
    for(var i=0; i<addedTags.length; i++){
      tagList.push(addedTags[i].text);
    }
    */}
    var attached_tag_str = JSON.stringify(tagList);

    var url;
    var action = $('#action').val();
    if(action ==='add'){
      url = BASE_URL + 'group/'.concat(groupid,'/newEvent');
    }else{
      url = BASE_URL + 'group/'.concat(groupid, '/event/', $('#eventid').val(), '/eventDoEdit');
    }
    if (is_need_publish){
    	if (!confirm("The event invitation will be sent to all the group members by email, are you sure ?")){
    		return;
    	}
    }

    $.post(url,{
      Topic: topic,
      Group: groupid,
      Address: address,
      beginDate: beginDate,
      BeginTime: beginTime,
      endDate: endDate,
      EndTime: endTime,
      EventDetail: eventDetail,
      Tag: attached_tag_str,
      Publish: is_need_publish,
    })
      .done(function(data){
        if(data.error){
          $('#errMsgLabel').text(data.error);
          $('#errMsgLabel').show();
          $('#errMsgDiv').show();
        }else{
          //Redirect the location if the page was redirected to login page.
          if ($(data).has('#login_form').length) {
            location.href = '/login'; //TODO potential bug? 
          }else{            	
						if(confirm("Operation Succeeded. Do you want to redirect to event page?")){	
							if (action === 'edit'){
							  location.href = '#/group/show/'+$('#groupid').val()+'/eventshow/'+ $('#eventid').val();
							}else if (action === 'add'){							
								location.href = '#/group/show/'+$('#groupid').val()+'/eventshow/'+ data.id; 
							}
							
						}	                                
          }
        }
      })
      .fail(function(xhr, status, errorThrown){
        console.log(status + errorThrown);
      });
  }	
  
  cancelEvent(){
    if(confirm("The event creation or modification process will be terminated, are you sure?")){							
			location.href = '#/group/show/'+$('#groupid').val()+'/eventshow/'+ $('#eventid').val();							
		}
  }
	
	render(){    
		
	  const{
	    groupid,
	    eid,
	    action
	  } = this.props;	  
	  
	  //console.log("this.state.targetgroup.name is"+this.state.targetgroup.name); 
	  
    switch (action){
    	case 'add':
    	  var eventTitle = 'New Event';    	      	      	  
    	  var dftTime = this.defaultTime();
    	  break;
			case 'edit':
    	  var eventTitle = 'Edit Event';    	  
    	  
		    if (this.state.targetevent.begindate) {
		    	//alert(this.state.targetevent.begindate);
		    	var bgdate = new Date(Date.parse(this.state.targetevent.begindate));
					var bgdate = bgdate.getFullYear()  + '-' + (bgdate.getMonth() + 1) + '-' + bgdate.getDate();
					
					var dataobj = Common.fulltime(this.state.targetevent.begindate);
					var b_hours = dataobj.hours;
					var b_minutes = dataobj.minutes;
					
					var bgtime = bgdate + " " + b_hours + ":" + b_minutes;
					//alert("bgtime is:" + bgtime);
				}
		    
		    if (this.state.targetevent.enddate) {
		    	var todate = new Date(Date.parse(this.state.targetevent.enddate));
					var todate = todate.getFullYear()  + '-' + (todate.getMonth() + 1) + '-' + todate.getDate();
					
					var dataobj = Common.fulltime(this.state.targetevent.enddate);
					var d_hours = dataobj.hours;
					var d_minutes = dataobj.minutes;
					var endtime = todate + " " + d_hours + ":" + d_minutes;
					//alert("endtime is:" + endtime);					
				}    
		 	    	  
    	  break;
    	default: 
    	  var eventTitle = 'Unknown Title';
    }		
    

		return(
		<div className="row">	
			<input id="eventid" type="hidden" value= {this.state.targetevent&&this.state.targetevent.id} />
			<input id="action" type="hidden" value={action} />
			<input id="groupid" type="hidden" value={groupid} />
			{/*
			<div className="input-append date form_datetime">
		    <input size="16" type="text" value="" />
		    <span className="add-on"><i className="icon-th"></i></span>
      </div>
		  */}
			<div className="container-fluid">
			  <div className="row">
			    <div className="col-md-12">
			      <div className="page-header">  
			        <h3>{eventTitle}</h3>
			      </div>
			    </div>
			  </div>
			  <div className="form-group" >  
		      <div id="errMsgDiv" className="alert alert-danger alert-dismissible" role="alert" style={{display:"none"}}>
            <button type="button" className="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
            <label id="errMsgLabel"></label>
		      </div>
			  </div>
			  <div className="row">
			    <div className="col-md-12">
			      <form className="form-horizontal" id="EventForm1" style={{marginTop:"10px"}}>
			          <div className="form-group">
		              <label htmlFor="inputTopic" className="col-sm-2 control-label">Topic</label>
		              <div className="col-sm-10">
		              <input type="text" className="form-control" id="inputTopic" name= "Topic" value={this.state.targetevent.topic?this.state.targetevent.topic:''} onChange={this.handleInputChange} placeholder="" />
		              </div>
			          </div>
			          <div className="form-group">			              
			              <div className="col-sm-3" style={{display:"none"}}>
			                  {/*
			                  <select className="form-control" id="selectGroup" name="Group" placeholder="">
			                  <% for(var i=0; i<group.length; i++) {%>
			                      <option><%= group[i].name %></option>
			                  <% } %>                               
			                  </select>
			                  */}
			              </div>
			              
			              <label htmlFor="inputAddress" className="col-sm-2 control-label">Address</label>
			              <div className="col-sm-10">
			                  <input type="text" className="form-control" id="inputAddress" name="Address" value={this.state.targetevent.address?this.state.targetevent.address:''} onChange={this.handleInputChange} placeholder="" />
			              </div>
			          </div>
			          <div className="form-group">
			              <label htmlFor="inputBeginTime" className="col-sm-2 control-label">Begin Time</label>
			              <div className="col-sm-4">
			                {
			                	(this.state.targetevent.begindate) ? 
			                	(<input type="text" className="form-control" id="inputBeginTime" name= "beginDate" value={bgtime} placeholder="" />)												
			                	:
			                  (<input type="text" className="form-control" id="inputBeginTime" name= "BeginTime" value={dftTime} onChange={this.handleTimeChange} placeholder="" />)
			                  			               
			                }
			              </div>
			              
			              <label htmlFor="inputEndTime" className="col-sm-2 control-label">End Time</label>
			              <div className="col-sm-4">
			                {(this.state.targetevent.enddate)?
			                  (<input type="text" className="form-control" id="inputEndTime" name= "endTime" value={endtime} placeholder="" />)
			                  :
			                  (<input type="text" className="form-control" id="inputEndTime" name= "endTime" value={dftTime} onChange={this.handleTimeChange} placeholder="" />)			                
			                }
			              </div>			              
			          </div>
			        			          
		            <div className="form-group">
			            <label htmlFor="editor" className="col-sm-2 control-label">Event</label>
			            <div className="col-sm-10" id="editor" name="eventDetail">
			              <div id="group-desc">
                      {this.loadDesc()}
			              </div>	
		              </div>	 
                  <textarea id="hiddeneditor" style={{display:"none"}} defaultValue=""></textarea>			              
		            </div>			          
			          
			          <div className="form-group">
			            <label htmlFor="inputtags" className="col-sm-2 control-label">Tags</label>
			            <div className="col-sm-6">
			              <div className="pillbox" data-initialize="pillbox" id="myPillbox">
			                <ul className="clearfix pill-group">
			                  ....
			                  <li className="pillbox-input-wrap btn-group">
			                    <a className="pillbox-more">and <span className="pillbox-more-count"></span> more...</a>
			                    <input type="text" className="form-control dropdown-toggle pillbox-add-item" placeholder="add tags"/>
			                    <button type="button" className="dropdown-toggle sr-only">
			                      <span className="caret"></span>
			                      <span className="sr-only">Toggle Dropdown</span>
			                    </button>
			                    <ul className="suggest dropdown-menu" role="menu" data-toggle="dropdown" data-flip="auto"></ul>
			                  </li>
			                </ul>
			              </div>
			              <input id="attached_tags_json" type="hidden" value={this.state.attached_tags_json} />
			            </div>			            			            
			          </div>
			
			          <div className="form-group">
		              <div className="col-sm-offset-3 col-sm-10">
		                <button type="button" id="save-event" className="btn btn-primary btn-lg" onClick = {this.saveEvent.bind(this,false)} form="EventForm1">Save</button>
		                <button type="button" id="publish-event" className="btn btn-primary btn-lg" onClick = {this.saveEvent.bind(this,true)}>Publish</button>
		                <button type="button" className="btn btn-primary btn-lg" onClick={this.cancelEvent}>Cancel</button>
		              </div>				             		
			          </div>
			      </form>
			    </div>
			  </div>
			</div>
		</div>	
	    )
	  }
}

export default connect((state, ownProps) => ({
	existedGroups: state.group.allGroups,
	auth: state.auth
}))(EventMgr)
