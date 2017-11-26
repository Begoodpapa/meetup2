'use strict';
var React = require('react');
var Dropzone = require('react-dropzone');
var ICSParse = require('../../../api/services/ICSParse.js');
var EventForm = require('../component/EventForm.jsx');


var DropzoneDemo = React.createClass({

  componentDidMount: function() {

    var self = this;
    $.getJSON('/api/group')
      .done(function(res, xhr) {
        console.log('resxxxx', res);
        self.replaceState({
          groups: res,
          step: 1
        });
        console.log('logsgroup', self.state.groups);
      })
      .fail(function(res) {
        console.error('getJSON', err.status, res.statusText, res.responseText);
      });

  },

  getInitialState: function() {
    return {
      event: {},
      groups: [],
      step: 1
    };
  },

  onDrop: function(files) {
    console.log('Received files: ', files);
    var formData = new FormData();
    formData.append('ics', files[0]);
    var self = this;
    var reader = new FileReader();

    if (files.length === 0) {
      return;
    }
    reader.onload = function(e) {
      var text = reader.result;
      console.log('err', e, text.length);
      var event = ICSParse.icsStringtoEvent(text);

      self.replaceState({
        event: event,
        step: 2,
        groups: self.state.groups
      });
      self.calenderFile = files[0];
      console.log('after drop', self.state.groups);
    };
    reader.readAsText(files[0], 'utf-8');
  },

  postClaneder: function(e) {
    e.preventDefault();

    console.log('logsxxx', React.findDOMNode(this.refs.theInput));


    console.log('logs', e);
    console.log('post', this.calenderFile);
    var formData = new FormData();
    formData.append('ics', this.calenderFile);
    formData.append('group', $('#group').val());
    $.ajax({
      type: 'POST',
      url: '/event/s',
      data: formData,
      processData: false,
      contentType: false
    }).done(function(res, textStatus, xhr) {
      console.log('msg', res);
      window.location.href = 'event/show/' + res.id
    }).fail(function() {
      console.log('logs', arguments);
    });

  },


  render: function() {
    var view;
    if (this.state.step === 1) {
      view = (<Dropzone onDrop={this.onDrop} size={150}>
                <div>Try dropping Caldender file(*.ics),
                  <br/> or click to select files to upload.</div>
              </Dropzone>);
    } else {
      console.log('debug', this.state.groups);
      view = <EventForm event={this.state.event} onClick={this.postClaneder} groups={this.state.groups} />
    }

    return view;
  }
});

React.render(<DropzoneDemo />, document.getElementById('createEvent'));
