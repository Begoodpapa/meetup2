'use strict';
var async = require('async');
var gm = require('gm');
var path = require('path');

module.exports = {
  //Resize the given image to different sizes.
  resizeTo: function(imgPath, sizes, cb){
    var dirname = path.dirname(imgPath);
    var basename = path.basename(imgPath);
    var resizeImg = function(size){
      return function(callback){
        var imgName = size[2].concat('_', basename);
        var newPath = path.join(dirname, imgName);
        gm(imgPath)
          .resize(size[0],size[1])
          .write(newPath, function(err){
            if(err)
            {
              sails.log.error('Resize and save image failed: ' + err);
              callback(err);
            }else{
              callback(null, imgName);
            }
          });
      }
    };

    var resizeArray = sizes.map(function(item){
      return resizeImg(item);
    });
    //Resize the image to different sizes parallelly.
    async.parallel(resizeArray, function(err, results){
      if (err) {
        sails.log.error(err);
        cb(err);
      }else{
        cb(null, results);
      }
    });
  }

}
