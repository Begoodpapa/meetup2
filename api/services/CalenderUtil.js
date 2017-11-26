'use strict';
var ORIGINAL_START_LABEL = '-----Original Appointment-----';
var DELIMETER = '\r\n';
function Invitation(rawText) {
  this._rawText = rawText;
  this.when = null;
  this.duration = 60;
  this.where = null;
  this.subject = null;
  this.body = null;

  this._isValid = true;
  this._mainMail = this.getMainMail();
  this._header = this.getMailHeader();


};
Invitation.prototype.getMailHeader = function () {
  var header= this._mainMail.split(DELIMETER)
    .filter(function (part, index) {
      return index <= 5; // 5 items: from,to,sent,when,where,subject
    })
    .reduce(function(memo,headLine){
      var parts = headLine.split(':');
      memo[parts[0].toLowerCase()] = parts.slice(1).join(':').trim();
      return memo;
     },{});
  return header;
}
Invitation.prototype.getMainMail = function () {
  var startIndex = this._rawText.lastIndexOf(ORIGINAL_START_LABEL);
  if (startIndex === -1) {
    return this._rawText;
  } else {
    return this._rawText
      .substring(startIndex + ORIGINAL_START_LABEL.length, this._rawText.length)
      .trim();
  }
};
Invitation.prototype.toJSON = function () {
  var self = this;
  return {
//    when: self.when,
//    duration: self.duration,
//    where: self.where,
//    subject: self.subject,
    body: self._mainMail
  }
};
module.exports = {

  text2Meetup: function (text) {
    var invitation = new Invitation(text);
    return invitation;
  }

};