'use strict';
/**
 * @description :: Server-side logic for managing(preview, upload...) photos
 */
var path = require('path');
var url = require('util');
var _=require('lodash');
var photoRootDir = sails.config.upload.photo.root;
var photoMaxSize = sails.config.upload.photo.maxSize * 1000000;
var smallSize = sails.config.upload.photo.smallSize;
var thumbSize = sails.config.upload.photo.thumbSize;
var mediumSize = sails.config.upload.photo.mediumSize;
var largeSize = sails.config.upload.photo.largeSize;

module.exports = {

  galary: function(req, res) {
    var gid = req.param('gid');
    var galary = [];
    var albumPath = url.format('/group/%s/album/', gid);
    Event.find({
        group: gid
      })
      .populate('photos')
      .exec(function(err, events) {
        if (err) {
          sails.log.error(err);
          return res.negotiate(err);
        }
        _(events).forEach(function(e) {
          var photos = e.photos;
          var href = albumPath + e.id;
          var noPhoto = photos === 'undefined' || photos.length === 0;
          var amount = noPhoto ? 0 : photos.length;
          var uploadhref = href + '/upload';
          var thumbnailhref = href + '/thumbnail';
          // var thumbnail = noPhoto ? '' : path.join(photoRootDir, photos[0].thumbnail);
          var href = noPhoto ? uploadhref : thumbnailhref;
          var album = {
            thumbnailhref: href,
            uploadhref: uploadhref,
            amount: amount,
            eventTime: e.begindate,
            // thumbnail: thumbnail,
            phoDescrip: e.phoDescription,
            topic: e.topic,
            photos: photos
          };
          galary.push(album);
        });
        return res.view('photos/GalaryOverview', {
          galary: galary,
          gid: gid,
          layout: null
        });
      });
  },

  thumbnail: function(req, res) {
    var eid = req.param('eid');
    Photo.findAllByAlbum(eid, function(err, result) {
      if (err) {
        return res.negotiate(err);
      }
      return res.view('photos/AlbumThumbnail', {
        photos: result.photos,
        album: result.album,
        layout: null
      });
    });
  },

  upload: function(req, res) {
    var eid = req.param('eid');
    var gid = req.param('gid');
    Event.findOne({
        id: eid,
        group: gid
      })
      .exec(function(err, event) {
        if (err) {
          return res.negotiate(err);
        }
        return res.view('photos/UploadPhotos', {
          album: event,
          layout: null
        });
      });
  },

  doUpload: function(req, res) {
    var gid = req.param('gid');
    var eid = req.param('eid');
    var imagesPath = url.format('%s/%s/%s/', photoRootDir, gid, eid);
    var uploadPath = path.join(sails.config.appPath, sails.config.assetsdir.directory, imagesPath);
    var options = {
      dirname: uploadPath,
      maxBytes: photoMaxSize //10M
    }
    req.file('file').upload(options, function whenDone(err, files) {
      if (err) {
        sails.log.error(err);
        return res.serverError(err);
      }
      // If no files were uploaded, respond with an error.
      if (files.length === 0) {
        sails.log.error('No file was uploaded');
        return res.badRequest('No file was uploaded');
      }
      //Only one file being uploaded at a time.
      var file = files[0];

      var getImagePath = function(imgName){
        return url.format('%s/%s/%s', gid, eid, imgName);
      }

      PhotoService.resizeTo(file.fd, [thumbSize,smallSize,mediumSize,largeSize], function(err, results){
        var original = getImagePath(path.basename(file.fd));
        var thumb = err ? original : getImagePath(results[0]);
        var small = err ? original : getImagePath(results[1]);
        var medium = err ? original : getImagePath(results[2]);
        var large = err ? original : getImagePath(results[3]);
        var photo = {
          original: original,
          large: original,
          medium: medium,
          small: small,
          thumbnail: thumb,
          origSize: file.size,
          origName: file.filename,
          origType: file.type,
          owner: req.session.user,
          album: eid
        };
        Photo.create(photo, function createPhoto(err, created) {
          if (err) {
            sails.log.error(err);
            return res.serverError(err);
          }
          return res.ok('upload and resize photo successfully.');
        });
      });
    });
  },

  preview: function(req, res) {
    var eid = req.param('eid');
    Photo.findAllByAlbum(eid, function(err, result) {
      if (err) {
        return res.negotiate(err);
      }
      return res.view('photos/AlbumPreview', {
        photos: result.photos,
        album: result.album
      });
    });
  }

};
