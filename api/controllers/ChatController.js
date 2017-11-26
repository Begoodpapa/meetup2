'use strict';
/**
 * ChatController
 *
 * @description :: Server-side logic for managing chats
 * @help        :: See http://links.sailsjs.org/docs/controllers
 */

module.exports = {

  get: function(req, res) {
    if (req.isSocket) {
      // sails.socket.
      sails.sockets.join(req.socket, 'room');

      res.json({
        question: 'where is love ?',
        id: 2
      });

    } else {
      res.view('askingRoom');
    }
  },

  post: function(req, res) {
    if (req.isSocket) {
      var question = req.body.question;

      sails.sockets.broadcast('room', {
        question: question
      });

      res.ok();

    } else {
      res.badRequest('socket only');
    }

  }


};
