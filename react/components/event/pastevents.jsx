'use strict';
import React from 'react';
var Common = require('../../common.js');

class PastEvents extends React.Component {

  getevents() {

    const {
      groupid,
      pastEvents
    } = this.props;

    var eventsarray = this.props.pastEvents.map(function(event) {

      let dateobj = Common.fulltime(event.begindate);
      let b_date = dateobj.localdate;
      let fulltime = dateobj.fulltime;

      let hlink = '#/group/show/' + groupid + '/eventshow/' + event.id;

      return(
        <li className="group-events-li" key={event.id}> 
          <div className="event-time"> 
            <h5> {b_date} </h5>
            <h5> {fulltime} </h5>  
          </div>  
          <div className="event-add-title-member"> 
            <div className="event-localtion">  {event.address} </div> 
              <div className="event-title">
                <a href = {hlink} >
                  {event.topic}
                </a>
              </div>
              <div className="event-members"> {event.user.length} <span>hacks Going</span> </div>
          </div> 
        </li>
      )
    })
    return eventsarray;
  }

  render() {

    const {
      pastEvents
    } = this.props;

    var c_events_num = this.props.pastEvents.length;
    //console.log("c_events_num is"+c_events_num);

    if(c_events_num > 0) {
      var eventsarray = this.getevents();
      return(
        <div className="group-event">
          <ul className="group-event-ul">
            {eventsarray}
          </ul>
        </div>
      )
    } else {
      return(
        <div className="group-event">
        <h2 style={{marginTop:'5px'}}> No Past Events </h2>
      </div>
      )
    }
  }
}

export default PastEvents