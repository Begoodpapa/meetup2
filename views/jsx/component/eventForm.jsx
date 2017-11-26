'use strict';
var React = require('react');
var EventForm = React.createClass({
  displayName: 'EventForm',
  render: function() {
    var event = this.props.event || {};
    var groups = this.props.groups || [];
    console.log('logsgroupOptions', groupOptions);
    var groupOptions = groups.map(function(group, i) {
      console.log('log group', group);
      return (<option key={ i } value={group.id}>
                {group.name}
              </option>)
    });

    return (
      <div>
        <form className='form-horizontal' id='EventForm1'>
          <div className='form-group'>
            <label htmlFor='inputOrganizer' className='col-sm-2 control-label'>
              Group
            </label>
            <div className='col-sm-8'>
              <select className='form-control' id='group' name='Group' placeholder='' ref='theInput' test='1'>
                {groupOptions}
              </select>
            </div>
          </div>
          <div className='form-group'>
            <div className='col-sm-offset-2 col-sm-10'>
              <button onClick={ this.props.onClick} type='submit' className='btn btn-default' form='EventForm1'>
                Share
              </button>
            </div>
          </div>
          <div className='form-group'>
            <label htmlFor='inputTopic' className='col-sm-2 control-label'>
              Topic
            </label>
            <div className='col-sm-8'>
              <input className='form-control' value={event.topic} disabled/>
            </div>
          </div>
          <div className='form-group'>
            <label htmlFor='inputDate' className='col-sm-2 control-label'>
              Start
            </label>
            <div className='col-sm-8'>
              <input value={event.start.toString()} className='form-control' disabled/>
            </div>
          </div>
          <div className='form-group'>
            <label htmlFor='inputDate' className='col-sm-2 control-label'>
              End
            </label>
            <div className='col-sm-8'>
              <input value={event.end} type='text' className='form-control' id='inputEndDate' name='endDate' placeholder='' disabled />
            </div>
          </div>
          <div className='form-group'>
            <label htmlFor='inputAddress' className='col-sm-2 control-label'>
              Address
            </label>
            <div className='col-sm-8'>
              <input value={event.address} type='text' className='form-control' id='inputAddress' name='Address' placeholder='' disabled />
            </div>
          </div>
          <div className='form-group'>
            <label htmlFor='inputEvent' className='col-sm-2 control-label'>
              Event
            </label>
            <div className='col-sm-8'>
              <textarea value={event.desc|| 'no content'} className='form-control col-sm-8' rows='10' id='inputEvent' name='Event' disabled></textarea>
            </div>
          </div>
        </form>
      </div>
    );
  }
});

module.exports = EventForm;