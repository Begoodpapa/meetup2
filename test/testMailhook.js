'use strict';
/* global CalenderUtil */
var expect = require('chai').expect;
describe('Mail hook Util', function() {

  var rawText = 'When: 2014年12月15日星期一 13:00-15:00 (UTC+08:00) Beijing, Chongqing, Hong Kong, Urumqi.\r\nWhere: Chongqing-External, 26F\r\n\r\nNote: The GMT offset above does not reflect daylight saving time adjustments.\r\n\r\n*~*~*~*~*~*~*~*~*~*\r\n\r\n\r\n\r\n-----Original Appointment-----\r\nFrom: Zhang, Yang 2. (NSN - CN/Hangzhou)\r\nSent: Thursday, December 11, 2014 5:25 PM\r\nTo: Zhang, Yang 2. (NSN - CN/Hangzhou); Wang, Gang-Layner (NSN - CN/Hangzhou); Zhou, Feng-Fred (NSN - CN/Hangzhou); Shi, Yuanmin Simon (NSN - CN/Hangzhou); Zhang, Eric (NSN - CN/Hangzhou); Shu, Pengfei (NSN - CN/Hangzhou)\r\nSubject: HZ Site coach meeting for ranking system\r\nWhen: 2014年12月15日星期一 13:00-15:00 (UTC+08:00) Beijing, Chongqing, Hong Kong, Urumqi.\r\nWhere: Chongqing-External, 26F\r\n\r\n\r\nWhen: 2014年12月15日星期一 13:00-15:00 (UTC+08:00) Beijing, Chongqing, Hong Kong, Urumqi.\r\nWhere: Chongqing-External, 26F\r\n\r\nNote: The GMT offset above does not reflect daylight saving time adjustments.\r\n\r\n*~*~*~*~*~*~*~*~*~*\r\n\r\nHi\r\n\r\nAfter our discussion, we have one picture of the ranking system:\r\nThere is on data sheet for one participant. It can be presented as a radar map; The participant can find the profile of him/her, and also can apply activities to promote level in the sheet.\r\nThen, ranking system can collect the expectation from participants, who wants to improve their level in some catalogs.\r\n\r\nExamples of Ranking system data sheet:\r\nCatalog Level 1, Learner        Level 2 Practicer       Level 3 Contributer     Level 4 Master  … …\r\nTDD\r\nUT\r\nATDD\r\nScrum\r\nTA\r\n… …\r\n\r\nAgenda:\r\n1.      To supply catalogs from your BL point of view, LE: 2014.12.16\r\n2.      To combine all catalogs\r\n3.      To groom how to implement Rank system, and make plan\r\n\r\n';

  var text = 'From: Zhang, Yang 2. (NSN - CN/Hangzhou)\r\nSent: Thursday, December 11, 2014 5:25 PM\r\nTo: Zhang, Yang 2. (NSN - CN/Hangzhou); Wang, Gang-Layner (NSN - CN/Hangzhou); Zhou, Feng-Fred (NSN - CN/Hangzhou); Shi, Yuanmin Simon (NSN - CN/Hangzhou); Zhang, Eric (NSN - CN/Hangzhou); Shu, Pengfei (NSN - CN/Hangzhou)\r\nSubject: HZ Site coach meeting for ranking system\r\nWhen: 2014年12月15日星期一 13:00-15:00 (UTC+08:00) Beijing, Chongqing, Hong Kong, Urumqi.\r\nWhere: Chongqing-External, 26F\r\n\r\n\r\nWhen: 2014年12月15日星期一 13:00-15:00 (UTC+08:00) Beijing, Chongqing, Hong Kong, Urumqi.\r\nWhere: Chongqing-External, 26F\r\n\r\nNote: The GMT offset above does not reflect daylight saving time adjustments.\r\n\r\n*~*~*~*~*~*~*~*~*~*\r\n\r\nHi\r\n\r\nAfter our discussion, we have one picture of the ranking system:\r\nThere is on data sheet for one participant. It can be presented as a radar map; The participant can find the profile of him/her, and also can apply activities to promote level in the sheet.\r\nThen, ranking system can collect the expectation from participants, who wants to improve their level in some catalogs.\r\n\r\nExamples of Ranking system data sheet:\r\nCatalog Level 1, Learner        Level 2 Practicer       Level 3 Contributer     Level 4 Master  … …\r\nTDD\r\nUT\r\nATDD\r\nScrum\r\nTA\r\n… …\r\n\r\nAgenda:\r\n1.      To supply catalogs from your BL point of view, LE: 2014.12.16\r\n2.      To combine all catalogs\r\n3.      To groom how to implement Rank system, and make plan';


  it('can parse calender main body', function() {
    // console.log(text);
    var invitation = CalenderUtil.text2Meetup(rawText);
    expect(invitation.toJSON()).to.deep.equal({
//      when: new Date(2014,12,15,13,0),
//      duration:60,
//      where: 'Chongqing-External, 26F',
      body:text
    });

    // console.log(invitation._header);
  });


});

describe('Mail Hook', function() {

});
