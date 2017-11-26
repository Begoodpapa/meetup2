'use strict'; 
import React from 'react'; 
var $ = require('jquery');
import {BASE_URL} from 'config';
require('../../../assets/vender/fullcalendar/dist/fullcalendar.min.js');
import classes from '../../../assets/vender/fullcalendar/dist/fullcalendar.css';

class FullCalendar extends React.Component {
	
	handleevents(){
		const {
      groupid,
      events
    } = this.props;
  			
		//var c_events_num = this.props.events.length;
		//console.log("evnets number is"+c_events_num);  	
  	
  	var eventsarray = events.map(function(item){
  		var eventobj = {
  			title: item.topic,
  			start: item.begindate,
  			end: item.enddate
  		}
  		return eventobj;
  	})
  	
		$(document).ready(function() { 
			$('#calendar').fullCalendar('destroy');
		  $('#calendar').fullCalendar({ 
		    //set options and callbacks
		    events: eventsarray   
		    //TODO: event hyperlink to be added
		  }) 		 
		})  		
	}
	
	componentDidUpdate(){
		this.handleevents();
	}
	
	componentDidMount(){
		this.handleevents();
	}
	
  render(){
  	
  	return(
      <div id='calendar'></div>  
  )}

}

export default FullCalendar