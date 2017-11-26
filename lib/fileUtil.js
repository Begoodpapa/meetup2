'use strict';
var fs = require('fs');

module.exports = {

  //fileHd means the file handler, for example req.file('filename')
  fileUpload: function(fileHd, targetDir, saveAs, cb){

    //to open file to check if the file already existed, err means the file is not existed
    fs.open(targetDir+'/'+saveAs, 'r', function(err, fd){
      
      if(err){
        fileHd.upload({
          dirname: targetDir,
          saveAs: saveAs
        }, function(err, files) {
          if (err) {
            return cb(err);
          }
          if (files.length === 0) {
            return cb('no file saved');
          }
          return cb(null);
        });
      }else{
        fs.close(fd, function(err){
          return cb('file is already existed');  
        });
      }

    });
    
  },

  getAllImages: function(dir, cb){

    var fileList = [];
    var called = 0;

    (function walk(path, upperDir){  
        called++;
        fs.readdir(path, function(err, dirList){
          if(err){
            return cb(err, fileList);
          }
          if(dirList.length===0){
            called--;
            //when called equal 0, means current invoke is the final one
            if(called===0){
              return cb(null, fileList);
            }
          }else{
            async.map(dirList, function(e, cb){fs.stat(path+'/'+e, cb);}, function(err, results){
              results.forEach(function(result, index){
                if(index === results.length-1){
                  called--;  
                }
                if(result.isFile()){
                  var fileObj = {};
                  fileObj.is_dir = false;
                  fileObj.is_photo = true;
                  fileObj.filesize = result.size;
                  fileObj.datetime = result.ctime;
                  fileObj.has_file = false;
                  if(upperDir==='/'){
                    fileObj.filename = dirList[index];
                  }else{
                    fileObj.filename= upperDir+'/'+dirList[index];
                  }
                  fileList.push(fileObj);   
                  //when called equal 0 and the element is the last element in results,
                  //then means current invoke is the final one
                  if((called===0)&&(index === results.length-1)){
                    return cb(null, fileList);
                  }
                }else{
                  walk(path+'/'+dirList[index], dirList[index]);
                }
              })
            });
          }  
        });
    })(dir, '/');

  },

}