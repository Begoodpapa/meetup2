'use strict';
/**
 * UploaderController
 *
 * @description :: Server-side logic for managing uploaders
 * @help        :: See http://links.sailsjs.org/docs/controllers
 */

module.exports = {



  /**
   * `UploaderController.event()`
   */
  event: function(req, res) {
    console.log('logs', req.files);
    console.log('logs', req.body);
    console.log('logs', req.param());
    var icsFile = req.file('ics');
    icsFile.upload(function onUploadComplete(err, files) {
      //  Files will be uploaded to .tmp/uploads

      if (err) {
        return res.negotiate(err);
      }
      //  IF ERROR Return and send 500 error with error

      console.log(files);
      res.json({
        status: 200,
        file: files
      });
    });

  }
};