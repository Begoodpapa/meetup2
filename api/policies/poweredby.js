'use strict';

module.exports = function poweredByCoach(req, res, next) {
  res.set('X-Powered-By', 'All contributors with love');
  next();
};
