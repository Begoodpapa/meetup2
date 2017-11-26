'use strict';

module.exports = function socketOnly(req, res, next) {

  if (req.isSocket) {
    return next();
  }
  return res.badRequest();

};
