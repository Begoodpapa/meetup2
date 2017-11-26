'use strict';
var icsParser = require('vdata-parser');
var fs = require('fs');

// For some keys contain ";", remove the right part
// eg: DTSTART;TZID=China Standard Time => DTSTART
var purifyKeys = function(vData) {
  for (var key in vData) {
    if (vData.hasOwnProperty(key)) {
      var index = key.indexOf(';');
      if (index !== -1) {
        var value = vData[key];

        vData[key.slice(0, index)] = value;
        delete vData[key];
      }
    }
  }
};

var textify = function(string) {
  return string.replace(/\\n/g, "\r\n")
    .replace(/\\,/g, ',');
};

// TODO: consider different timezones
var timeOffsetInMinutes = new Date().getTimezoneOffset();

var DT2Date = function(str) {
  var reg = /^(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})\w*$/;
  var matchs = reg.exec(str);
  matchs = matchs.slice(1);

  var year = parseInt(matchs[0]);
  var month = parseInt(matchs[1]);
  var date = parseInt(matchs[2]);
  var hour = parseInt(matchs[3]);
  var minute = parseInt(matchs[4]);
  var second = parseInt(matchs[5]);

  return new Date(year, month - 1, date, hour, minute, second);
};


module.exports = {

  icsFiletoEvent: function(fileName, callback) {
    var self = this;
    fs.readFile(fileName, 'utf-8', function(err, content) {
      if (err) {
        return callback(err);
      }

      self.vcal2Event(content, function(err, event) {
        if (err) {
          return callback(err);
        } else {
          callback(null, event);
        }
      });

    });
  },

  vcal2Event: function(string, callback) {
    try {
      var vEvent = icsParser.fromString(string).VCALENDAR.VEVENT;
      //console.log("vEvent: " + JSON.stringify(vEvent) );
      purifyKeys(vEvent);

      if (!vEvent.hasOwnProperty("SUMMARY")) { // sanity check
        throw new Error("Insufficient vEvent information.");
      } else {
        callback(null, {
          topic: vEvent.SUMMARY,
          desc: textify(vEvent.DESCRIPTION),
          start: DT2Date(vEvent.DTSTART),
          end: DT2Date(vEvent.DTEND),
          address: textify(vEvent.LOCATION)
        });
      }
    } catch (err) {
      callback(err);
    }
  }

};