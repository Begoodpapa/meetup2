'use strict';
/* global User, LDAPUtils*/

module.exports = {

  validateData: function(req, res, next) {
    var uid = req.body.uid;
    var password = req.body.password;
    if (uid && password && password.length > 0) {
      next();
    } else {
      req.flash('error', 'Invalid Credentials');
      return res.redirect('/login');
    }
  },

  logoutAjax: function(req, res) {
    req.session.user = null;    
    return res.json(200);
  },

  loginAjax: function(req, res) {
    var uid = req.body.uid;
    var password = req.body.password;
    if (!uid || !password) {
      return res.json(200, {error: 'Bad username or password'});
    }
   
    AuthService.auth(uid, password, function(err, user) {
      if(!err)
      {
        req.session.user = user;
        
        var m = new Date();
        var expireDate = new Date(m.getTime() + 1000 * 60 * 15); //session expire time = 15 minutes. unit of getTime is millisecond        
        //req.session.cookie.expires = expireDate; TODO enable session expiretime, and to design a mechnism to refresh session automatically if a user keeps active
        return res.json(200, {user: user});
      }else{
        console.log('login failed in loginAjax, userId:%s, error message: %s', uid, err.message);
        return res.json(200, {error: err.message});
      }
    });
  },

  login: function(req,res){

    res.clearCookie('oldurl');
    var result = AuthService.auth(req.body.uid,req.body.password, function(err, user) {
      if(err)
      {
        console.log('login failed in login, userId:%s, error message: %s', req.body.uid, err.message);
        req.flash('error', err.message);
        return res.redirect('/login');
      }else{
        req.session.user = user;

        var groupid='';
        var cookies = req.cookies;
        var fromurl = cookies.oldurl;
        var tourl = '/';
        var urlStrs=[];

        if(!fromurl) {
          return res.redirect(tourl);
        }

        urlStrs = fromurl.split('/');

        /*If the first word of url is not group, then means the url has none relation with
         *the group workspace in front end, we just need return the saved old url,
         *otherwise we need to assemble the new url to satisfy the front-end framework
         * which is based on hash change
         */

        if(urlStrs[1]!=='group'){
          tourl = fromurl;
        }else{
          groupid = urlStrs[2];
          if (fromurl.indexOf('addgroupuser') > 0) {
            tourl = '/group/show/'+ groupid+'#/group/'+groupid+'/members';
          }else if (fromurl.indexOf('addMemberAjax') > 0) {
            tourl = '/group/show/'+ groupid+'#/group/'+groupid+'/members';
          }
          else{
            tourl = '/group/show/'+groupid+'#'+fromurl;
          }
        }

        return res.redirect(tourl);

      }
    });
  },
  
  getStatusAjax: function(req, res){

    res.set('Cache-Control', 'private, max-age=0, no-cache');
    if(req.session.user){
      var user = req.session.user;
      User
        .findOne({_id:user._id})       
        .then(function (user) {
          return res.json(200, {user: user});
        })
        .catch(function(err){
          sails.log.error(err);
        })
    }else{
        return res.json(200, {err: 'user not logged in'});
    }
  }  

};
