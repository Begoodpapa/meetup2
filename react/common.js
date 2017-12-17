import { BASE_URL } from 'config';
var $ = require('jquery');
import React from 'react';

module.exports = {

  fulltime: function(date) {

    let begindate = new Date(date);
    let localdate = begindate.toLocaleDateString();
    let hours = begindate.getHours();

    if(hours < 10) {
      hours = '0' + hours;
    }
    let minutes = begindate.getMinutes();
    if(minutes < 10) {
      minutes = '0' + minutes;
    }

    let fulltime = hours + ':' + minutes;
    //console.log("fulltime is"+fulltime);
    //console.log("localdate is"+localdate);
    return {
      fulltime: fulltime,
      localdate: localdate,
      hours: hours,
      minutes: minutes
    };
  },

  parseDateTime: function(date) {
    let array = date.trim().split(" "); //the format is yyyy-mm-dd hh:mm, so use space as split label

    let datestr = array[0];
    let timestr = array[1];

    return {
      timestr: timestr,
      datestr: datestr
    };
  },

  getfilelist: function(groupid) {
    var url = BASE_URL + 'group/' + groupid + '/todownloadfile';
    var that = this;
    var error = {};
    var files = [];

    $.ajaxSetup({
      async: false
    });

    $.get(url, function(data, result) {
      if(data.error) {
        error = "Get file list error";
        files = null;

      } else if(data.files) {
        error = null;
        files = data.files;
      }
    })

    return {
      error: error,
      files: files
    };
  }
}