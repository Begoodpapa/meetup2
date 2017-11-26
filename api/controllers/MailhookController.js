'use strict';

function text2meetup(text) {

  var partials = text.split('\r\n');

  return {
    body: partials[partials.length - 1]
  };

}

module.exports = {

  hook: function(req, res) {

    var body = req.body;

    console.log(text2meetup(body.text));

    res.json({
      result: 'OK'
    });

  }

};