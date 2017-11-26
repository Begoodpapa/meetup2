'use strict';

module.exports = {

  showabout: function(req, res){
        return res.view('aboutus/aboutus');
  },

  showcontribution: function(req, res){

    var contributors, thirdparts;
    var fs = require('fs');

    fs.readFile('./assets/about/contributors.json', 'utf8', function (err, data) {
      if (err) {
       throw err;
      }
      var contributors = JSON.parse(data);
      fs.readFile('./assets/about/thirdparts.json','utf8',function(err, data){
        if(err){
          console.log('read thirdparts.json failed');
        }
        thirdparts = JSON.parse(data);
        return res.view('aboutus/thanks', {
          contributors: contributors,
          thirdparts: thirdparts
        });

      });

    });
  }
};
