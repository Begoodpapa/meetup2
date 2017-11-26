'use strict';

module.exports = function(req, res, next) {

	if (req.session.user) {
		return next();
	}
  res.cookie('oldurl', req.url);
  //to return json format info in case client ask json response
  if(req.accepted[0].value==='application/json'){
    return res.json(200,'/login');
  }
	//return res.redirect('/login');
	return res.json(200, {error:"you need to sign in before this operation"});
};
