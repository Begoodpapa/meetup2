'use strict';
/**
 * CommentController
 *
 * @description :: Server-side logic for managing Comments
 * @help        :: See http://links.sailsjs.org/docs/controllers
 */

module.exports = {
	
  /**
   * `CommentController.show()`
   */
  show: function (req, res) {
    
    var eventID = req.param('relevantid');
    var category = req.param('category');

    Comment.find({ 
      where: { relevantid: eventID, category: category, replyto: '0'}, sort: 'createdAt DESC' 
    }).populate('likeby').populate('createdby').populate('replyto').exec( function( err, comments) {
      if( err ){          	 
        sails.log.error(err);
        //return res.negotiate(err);
        return res.json( 200, {error: err} );
      }else{                 
        return res.json( 200, JSON.stringify( comments ) );
      }
    });
  },

  showReplies: function (req, res) {
    
    var user = req.session.user;
    var maincommentid = req.param('id');

    Comment.find({ 
        where: { maincomment: maincommentid}, sort: 'createdAt ASC' 
    }).populate('likeby').populate('createdby').populate('replyto').exec( function( err, replies ) {
       if( err ){
         console.log('Get All replies under Comments error :', err);
         return res.negotiate(err);
       }else{
         return res.json( JSON.stringify( replies ) );
       }
    });
  },

  /**
   * `CommentController.create()`
   */
  create: function (req, res) {
    
    /* Need to add access right */
    var user = req.session.user;
    
    if (!user) {
    	err = 'User is not logged in. Comments post failed.';
      sails.log.error( err );
      return res.json( 200, {error: err} );
    }
    
    var relevantid = req.param('relevantid');
    var category = req.param('category');

    var newComment = {};
    newComment.relevantid = relevantid;
    newComment.content = req.body.content;
    newComment.likecount = 0;
   
    newComment.createdby = user.id;
    newComment.category = category;
    newComment.replyto = req.body.replyto;
    newComment.maincomment = req.body.maincomment;

    Comment.create( newComment, function ( err, created ){
      if( err ){
        sails.log.error( err );
        return res.negotiate( err );
      }
      
      Comment.findOne({id: created.id}).populate('likeby').populate('createdby').populate('replyto').exec( function( err, comment ){ 
        return res.json(JSON.stringify(comment));
      });      
    });      
  },


  /**
   * `CommentController.delete()`
   */
  delete: function (req, res) {

    var user = req.session.user;
    var commentID = req.param('id');
    Comment.destroy( { OR: [
                            { id: commentID },
                            { maincomment: commentID },
                            { replyto: commentID }
                           ]}).exec( function ( err, comment ){

     /* Shall we care the error of destroy? */
      return res.json(200);
    });
  },


  /**
   * `CommentController.like()`
   */
  getLike: function (req, res) {
    /* Need to add access right */
    var user = req.session.user;
    var commentID = req.param('id');
    var index = 0;

    var liked = false;
    Comment.findOne( { id: commentID }).populate('likeby').exec( function ( err, comment ){
      if( err || !comment ){
        sails.log.error( err );
        return res.negotiate( err );
      }

      /* find wether current user is in likedlist */
      for ( index = 0; index < comment.likeby.length; index ++){
          if( comment.likeby[index].id == user.id ){
              liked = true;
          }
      }

      return res.json( {userid: user.id, liked: liked, likecount: comment.likeby.length });
    });

  },


  /**
   * `CommentController.updateLike()`
   */
  updateLike: function (req, res) {
    /* Need to add access right */
    var user = req.session.user;
    var commentID = req.param('id');
    var liked = req.body.liked == "false" ? false : true;
    var likedcount = 0;

    Comment.findOne( { id: commentID }).populate('likeby').exec( function ( err, comment ){
      if( err || !comment ){
        sails.log.error( err );
        return res.negotiate( err );
      }
      likedcount = comment.likeby.length;

      if( liked ){
        comment.likeby.add(user.id);
        likedcount += 1;
      }else{
        comment.likeby.remove(user.id);
        likedcount -= 1;
      }
      comment.save( function( err ){
        if( err || !comment ){
          sails.log.error( err );
          return res.negotiate( err );
        }
        return res.json({liked: liked, likecount: likedcount});
      });
    });
  },


  /**
   * `CommentController.reply()`
   */
  reply: function (req, res) {
    return res.json({
      todo: 'reply() is not implemented yet!'
    });
  }
};

