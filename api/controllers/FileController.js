/**
 * FileController
 *
 * @description :: Server-side logic for managing files
 * @help        :: See http://links.sailsjs.org/docs/controllers
 */

module.exports = {

  toManageFile: function(req, res){

    var groupid = req.param('gid');
    File.find({group: groupid}).populate('owner').exec(function(err, files){
      if(err){ return res.negotiate(err);}
      return res.view('file/uploadAndDeleteFile', {
        files:files,
        groupid: req.param('gid'),
        layout:null
      });
    });

  },


  uploadFile: function (req, res) {

    var user = req.session.user;
    var file ={};
    file.name = req.file('groupfile')._files[0].stream.filename;
    file.owner = req.session.user;
    file.desc = req.param('filedesc');
    file.group = req.param('gid');
    file.downloads = 0;

    req.file('groupfile').upload({
      dirname: sails.config.appPath+'/assets/groupfile', 
      saveAs:req.file('groupfile')._files[0].stream.filename}, 
      function (err, uploadedFiles){
        if (err) {return res.send(500, err);}

        File.create(file).exec(function(err, createdFile){
          if(err) { 
            return res.negotiate(err);
          }
          return res.json(200, {username: user.fullname, id: createdFile.id});
        });

    });
  },

  destroyFile: function(req, res){
    var fs = require('fs');
    var fileID = req.param('fileid');
    
    File.destroy({id: fileID}, function(err, deleteds){

      if(err){ return res.negotiate(err);}
      if(deleteds.length===0){return res.json(200);}
      
      var deletedFile = deleteds[0];
      fs.exists('./assets/groupfile/'+deletedFile.name, function(existed){
        if(existed){
          fs.unlink('./assets/groupfile/'+deletedFile.name, function(err){
            if(err){console.log(err);}
            return res.json(200);
          });
        }else{
          return res.json(200);
        }
      });
      
    });
  },
  /*
  toDownloadFile: function(req, res){

    var groupid = req.param('gid');

    File.find({group: groupid}).sort({"downloads":-1}).populate('owner').exec(function(err, files){
      if(err){ return res.negotiate(err);}
      return res.view('file/downloadFile.ejs', {
        files:files,
        groupid: groupid,
        layout:null
      });
    });

  },
  */
  toDownloadFile: function(req, res){

    var groupid = req.param('gid');

    File.find({group: groupid}).sort({"downloads":-1}).populate('owner').exec(function(err, files){
      if(err){ return res.negotiate(err);}
      return res.json(200, {
        files:files               
      });
    });

  },

  downloadFile: function(req, res){
    var fs = require('fs');
    var mime = require('mime');
    var path = require('path');
    var fileID = req.param('fileid');
    
    File.find({id:fileID}, function(err, founds){
      if(err){
        console.log(err);
        return res.serverError('Download file failed in database inquery, fileID: ' + fileID);
      }else{
        if(founds.length===0){
          console.log('fileId %s was not found in server', fileID);
          return res.serverError('File not found in server, fileID: ' + fileID);
        }

        var filepath = './assets/groupfile/'+founds[0].name;
        fs.stat(filepath, function(err, stat){
          if(err){
            console.log(err);
            return res.notFound('File not found in server, please contact administrator. fileID: ' + fileID);
          }else{          	
            var stream = fs.createReadStream(filepath);
            res.setHeader('Content-Type', mime.lookup(filepath));
            res.setHeader('Content-Length', stat.size);
            res.setHeader('Content-Disposition', 'attachment; filename="' +path.basename(filepath)+'"');
            res.writeHead(200);
            stream.pipe(res);

            var new_downloads = founds[0].downloads + 1;
            File.update(fileID, {
              downloads: new_downloads,
            }).exec(function(err, updated) {
              if (err) {
                sails.log.error('file downloads update err');
              }
            });
          }
        })
      }
    });
  },

  getdownloads: function(req, res){
    var fileID = req.param('fileid');
    File.find({id:fileID}, function(err, founds){
      if(err){
        console.log(err);
      }else{
        return res.json(200, {downloads: founds[0].downloads});
      }
    });
  },

}