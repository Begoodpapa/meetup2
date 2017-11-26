'use strict';
var expect = require('chai').expect;
var fs = require('fs');
var path = require('path');

describe('service ICS to Event', function() {

  before(function() {
    this.icsStringtoEvent = sails.services.icsparse.icsStringtoEvent;
  });

  it('should parese real invitation ics file', function() {
    var icsContent = fs.readFileSync(
      path.join(__dirname, 'invitation.ics'), 'utf8');

    expect(this.icsStringtoEvent).to.be.ok;
    var event = this.icsStringtoEvent(icsContent);

    expect(event).to.have.keys(['topic', 'desc', 'end', 'start',
      'address'
    ]);
    expect(event.start).to.deep.equal(new Date(2015, 3 - 1, 10, 16, 0));
    expect(event.end).to.deep.equal(new Date(2015, 3 - 1, 10, 17, 0));
    expect(event.desc).not.contain('undefined');
  });

});