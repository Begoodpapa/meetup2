var React = require('react');
var CommentBox = React.createClass({displayName: "CommentBox",

  loadCommentsFromServer: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      success: function( data ){
        this.setState({data: JSON.parse(data)});
      }.bind( this ),
      error: function( xhr, status, err ){
        console.error( this.props.url, status, err.toString());
      }.bind( this )
    });
  },
 
  handleCommentSubmit: function( comment ){
    //Submit to server and refresh the list
    var comments = this.state.data;

    $.ajax({
      url: this.props.url,
      dataType: 'json',
      type: 'POST',
      data: comment,
      success: function(data) {
        comments.unshift(JSON.parse(data));
        this.setState({data: comments});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },

  handleCommentDelete: function( commentid ){
    var i = 0;
    var comments = this.state.data;
    var newComments = [];

    for(; i < comments.length; i++){
      if( comments[i].id != commentid ){
        newComments.push(comments[i]);
      }
    }
    //Submit to server and refresh the list
    $.ajax({
      url: this.props.url + commentid + '/delete',
      dataType: 'json',
      success: function(data) {
        this.setState({data: newComments});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },

  getInitialState: function(){
    return { data: []};
  },
  componentDidMount: function() {
    this.loadCommentsFromServer();
    //setInterval( this.loadCommentsFromServer, this.props.pollInterval);
  },

  render: function(){

    return (
      React.createElement("div", null, 
        React.createElement(CommentHeader, null), 
         userlogin ? React.createElement(CommentForm, {onCommentSubmit: this.handleCommentSubmit}) : null, 
        React.createElement(CommentList, {onCommentSubmit: this.handleCommentSubmit, onCommentDelete: this.handleCommentDelete, data: this.state.data, filter: this.state.filter})
      )
    );
  }
});

var CommentHeader = React.createClass({displayName: "CommentHeader",
  render: function(){
    var commentHeader;

    if( !userlogin ){
    commentHeader =  React.createElement("p", {id: "commentsPostExplain"}, React.createElement("a", {href: "#loginModal", "data-toggle": "modal", "data-backdrop": "static"}, " Login "), " to comment") ;
    }else{
    var greeting = "Hey, " + user.fullname + ", Join the conversation";
    commentHeader = React.createElement("h4", {className: "talk-heading margin-bottom"}, greeting) ;
    }

    return ( 
    React.createElement("div", null, 
     commentHeader 
    )
    );
  }
});

var CommentList = React.createClass({displayName: "CommentList",

  render: function(){      
    var onCommentSubmit = this.props.onCommentSubmit;
    var onCommentDelete = this.props.onCommentDelete;

    var commentNodes = this.props.data.map( function ( comment ){
        return ( 
        React.createElement(CommentReply, {key: comment.id, url: urlPrefix, comment: comment, onCommentSubmit: onCommentSubmit, onCommentDelete: onCommentDelete})
        );
     
    });

    return (
      React.createElement("ul", {className: "resetList dividedList comments"}, 
        commentNodes
      )
    );
  }
});    

var CommentReply = React.createClass({displayName: "CommentReply",
  getInitialState: function(){
      return { replyFormVisible: false,
               replyinfo: {replytoid: 0, maincommentid:0}};
  },

  showReplyForm: function( replyinfo ){
      this.setState({ replyFormVisible: true, replyinfo: replyinfo });
  },

  render: function(){      

    var showReplyForm = this.showReplyForm;
    var comment = this.props.comment;
    var replyto = this.state.replyinfo;
    var replyFormVisible = this.state.replyFormVisible;
    var replyUrl = urlPrefix + comment.id + "/replies";

    return (
        React.createElement("ul", null, 
        React.createElement(Comment, {comment: comment, onClickReplyButton: showReplyForm, onDeleteSubmit: this.props.onCommentDelete}), 
        React.createElement(ReplyList, {replyinfo: replyto, replyFormVisible: replyFormVisible, onClickReplyButton: showReplyForm, url: replyUrl, commentID: comment.id})
        )
    );
  }
});    

var CommentForm = React.createClass({displayName: "CommentForm",
  
  handleSubmit: function( e ){
    e.preventDefault();
    var text = this.refs.text.getDOMNode().value.trim();
    console.log( text );

    if( !text ){
      return;
    }
   
    // Send request to server
    this.props.onCommentSubmit({content: text, replyto: 0, maincomment: 0 });

    this.refs.text.getDOMNode().value = '';
    return;
  },

  render: function(){      
    return (
        React.createElement("div", {className: "figureset new-comment"}, 
          React.createElement(UserFigure, {user: user}), 
          React.createElement("div", {className: "figureset-description"}, 
            React.createElement("div", {className: "comment-wrap"}, 
              React.createElement("div", {className: "comment-input-wrap"}, 
                React.createElement("textarea", {name: "newComment", className: "j-comment-input J_onClick textInputTip span-100 hasMaxLen maxChars1000", title: "Ask a question, share something, or leave a comment...", placeholder: "Ask a question, share something, or leave a comment...", ref: "text"}), 
                 React.createElement("div", {className: "nib"}, 
                     React.createElement("div", {className: "inner-nib"})
                 )
              )
            ), 
            React.createElement("div", {className: "comment-actions"}, 
                React.createElement("button", {onClick: this.handleSubmit, className: "j-submit-comment button primary small"}, "Post")
            )
          )
        )
    );
  }
});    

var Comment = React.createClass({displayName: "Comment",

  getInitialState: function(){
  return {markhover: false};
  },

  handleReplyButton: function( event ){
    var replytoid = this.props.comment.id;
    var maincommentid = this.props.comment.id;

    if( this.props.comment.maincomment != 0 ){
      maincommentid = this.props.comment.maincomment;
    }

    this.props.onClickReplyButton( { replytoid: replytoid, maincommentid: maincommentid });
  },


  handleDeleteClick: function( event ){

    /*Update server info here */
    this.props.onDeleteSubmit(this.props.comment.id);
  },

  showDelete: function( event ){
    this.setState({markhover: true });
  },
  
  hideDelete: function( event ){
    this.setState({markhover: false });
  },
  render: function() {

    var monthArray = [ "Jan", "Feb", "Mar", "Apr", "May" , "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    var commentDate = new Date( this.props.comment.createdAt);
    var curDate = new Date();
    var commentDate4Show = monthArray[commentDate.getMonth()];
    var url = urlPrefix + this.props.comment.id + "/like";
    var commentID = this.props.comment.maincommentid ? this.props.comment.maincommentid : this.props.comment.id;
    var replyButtonHref = "#reply-form-to-" + commentID;

    if( ( curDate - commentDate ) < 1){
        commentDate4Show = "Just Now";
    }else if ( curDate.getFullYear() == commentDate.getFullYear() ){
        commentDate4Show = monthArray[commentDate.getMonth()] + " " + commentDate.getDate();
    }else{
        commentDate4Show = monthArray[commentDate.getMonth()] + " " + commentDate.getDate() + " " + commentDate.getFullYear();
    }

    return (
      React.createElement("li", null, 
        React.createElement("div", {className: "figureset"}, 
          React.createElement(UserFigure, {user: this.props.comment.createdby}), 
          React.createElement("div", {className: "figureset-description"}, 
            React.createElement("h5", null, 
            React.createElement(UserName, {user: this.props.comment.createdby}), 
            this.props.comment.maincomment && this.props.replytoUser ?" to ": null, 
            this.props.comment.maincomment && this.props.replytoUser ? React.createElement(UserName, {user: this.props.replytoUser}): null
            ), 
            React.createElement("div", {className: "comment-body"}, " ", React.createElement("p", null, this.props.comment.content)), 
            React.createElement("p", null, 
             userlogin ? 
            React.createElement(LikeWidget, {url: url, commentid: this.props.comment.id}) 
            : null, 
             userlogin ?  React.createElement(MidDot, null) : null, 
             userlogin ? 
            React.createElement("a", {onClick: this.handleReplyButton, className: "j-write-reply", href: this.replyButtonHref, "data-parent-id": "event_comment-450097011"}, "Reply") 
            : null, 
             userlogin ?  React.createElement(MidDot, null) : null, 
              commentDate4Show
            )
          ), 
           userlogin && this.props.comment.createdby.id == user.id ? 
          React.createElement("div", {className: "x-mark-cont clearfix", onMouseOver: this.showDelete, onMouseOut: this.hideDelete}, 
              React.createElement("div", {className: this.state.markhover? "x-mark hoverintent" : "x-mark"})
          ) 
          : null, 
           userlogin && this.props.comment.createdby.id == user.id ? 
          React.createElement("ul", {className: this.state.markhover? "resetList x-menu hoverintent" : "resetList x-menu", onMouseOver: this.showDelete, onMouseOut: this.hideDelete}, 
            React.createElement("li", null, React.createElement("a", {href: "#", onClick: this.handleDeleteClick, className: "deleter"}, "Delete"))
          ) 
          : null
        )
      )
    );
  }
});

var ReplyList = React.createClass({displayName: "ReplyList",

  getInitialState: function(){
      return { replies: [],
               showall: false };
  },

  loadRepliesFromServer: function() {
    $.ajax({
      url: urlPrefix + this.props.commentID + "/replies",
      dataType: 'json',
      success: function( data ){
        this.setState({replies: JSON.parse(data)});
      }.bind( this ),
      error: function( xhr, status, err ){
        console.error( this.props.url, status, err.toString());
      }.bind( this )
    });
  },

  componentDidMount: function() {
    this.loadRepliesFromServer();
  },

  handleReplySubmit: function( reply ){
    //Submit to server and refresh the list
    var replies = this.state.replies;

    $.ajax({
      url: urlPrefix,
      dataType: 'json',
      type: 'POST',
      data: reply,
      success: function(newReply) {
        var newReplies = replies.concat([JSON.parse(newReply)]);
        this.setState({replies: newReplies});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },

  handleReplyDelete: function( replyid ){
    //Submit to server and refresh the list
    var i = 0;
    var replies = this.state.replies;
    var newReplies = [];

    for(; i < replies.length; i++){
      if( replies[i].id != replyid && replies[i].replyto.id != replyid ){
        newReplies.push(replies[i]);
      }
    }

    $.ajax({
      url: urlPrefix + replyid + '/delete',
      dataType: 'json',
      success: function(data) {
        this.setState({replies: newReplies});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },


  showAllReplies: function( event ){
    this.setState({showall: true});
  },

  findReplytoUser: function( replyid , replyIndex ){
    var i = replyIndex > this.state.replies.length  - 1? this.state.replies.length  -1  : replyIndex;

    for( ; i >= 0; i--){
      if( this.state.replies[i].id == replyid ){
        return this.state.replies[i].createdby;
      }
    }
    return "";
  },

  render: function(){
    var onClickReplyButton = this.props.onClickReplyButton;
    var onDeleteSubmit = this.handleReplyDelete;
    var findReplytoUser= this.findReplytoUser;
    var filter = this.props.filter;
    var showcount = 0;
    var showall = this.state.showall;
    var replyID = "replyto-" + this.props.commentID;
    var replyIDHref = "#" + replyID;

    var replies = this.state.replies;

    var replyNode = replies.map( function ( reply ){
      if( !showall && showcount >= 2){
        return null;
      }
      var replyUserName = findReplytoUser( reply.replyto.id, showcount - 1);
      showcount += 1;
      return ( 
      React.createElement(Comment, {key: reply.id, comment: reply, onClickReplyButton: onClickReplyButton, onDeleteSubmit: onDeleteSubmit, replytoUser: replyUserName })
      );
    });

    return (
      React.createElement("li", {className: "replies"}, 
        React.createElement("ul", {id: this.replyID, className: "dividedList tight"}, 
             this.state.replies.length > 2 && !this.state.showall ? React.createElement("li", null, React.createElement("div", {className: "small leading-bottom"}, React.createElement("a", {href: this.replyIDHref, onClick: this.showAllReplies, className: "j-show-all-replies"}, "View all ",  this.state.replies.length, " replies"))) : null, 
           this.state.replies.length ? {replyNode} : null, 
           this.props.replyFormVisible ? React.createElement(ReplyForm, {onReplySubmit: this.handleReplySubmit, replyinfo: this.props.replyinfo, commentID: this.props.commentID})  : null
        )
      )
    );
  }
});

var ReplyForm = React.createClass({displayName: "ReplyForm",
  componentDidMount: function(){
      this.refs.replytext.getDOMNode().focus();
  },
  componentDidUpdate: function(){
      this.refs.replytext.getDOMNode().focus();
  },
  

  replySubmit: function( e ){
    var ENTER = 13;
    if( e.keyCode == ENTER || e.which == ENTER ){
      var reply = new Object();
      var text = this.refs.replytext.getDOMNode().value.trim();
      console.log( text );

      if( !text ){
        return;
      }

      reply.content = text;
      reply.maincomment = this.props.replyinfo.maincommentid;
      reply.replyto = this.props.replyinfo.replytoid;
      /* We just set these value for immediately show */
      reply.createdAt = 'Just Now';

      // Send request to server
      this.props.onReplySubmit(reply);

      this.refs.replytext.getDOMNode().value = '';
    }
    return;
  },

  render: function(){
   
    var id = "reply-form-to-"+ this.props.commentID;
    return (
      React.createElement("li", {id: id, className: "reply-wrap"}, 
        React.createElement("textarea", {onKeyPress: this.replySubmit, ref: "replytext", "aria-describedby": "enterDescribe", className: "reply-input textInputTip", title: "Write a reply..."}), 
        React.createElement("div", {className: "dot-loader-16 invisible"})
      )
    );
  }
});

var UserFigure = React.createClass({displayName: "UserFigure",
  render: function() {
    var userfd = this.props.user.userfd;

    if( !userfd ){
       userfd = "/images/default_upp.jpg";
    }
    var imgStyle = {
      color: 'green',
      display: 'block',
      backgroundImage: 'url(' + userfd + ')'
    };
    return (
      React.createElement("div", {className: "figureset-figure"}, 
          React.createElement("a", {href: "/user/myprofile", className: "mem-photo-background-60 square-50", style: imgStyle})
      )
    );
  }

});

var UserName = React.createClass({displayName: "UserName",
  render: function() {

    return (
      React.createElement("a", {href: "/user/myprofile", className: "memberinfo-widget", "data-memberid": this.props.user.id, title: this.props.user.fullname}, this.props.user.fullname)
    );
  }

});

var LikeWidget = React.createClass({displayName: "LikeWidget",

  getInitialState: function(){
  return {liked: false,
          likecount:0};
  },

  loadLikeFromServer: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      success: function( data ){
        this.setState( data);
      }.bind( this ),
      error: function( xhr, status, err ){
        console.error( this.props.url, status, err.toString());
      }.bind( this )
    });
  },
 
  handleLikeSubmit: function( likedata ){
    //Submit to server and refresh the list
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      type: 'POST',
      data:likedata,
      success: function(data) {
        this.setState(data);
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },

  componentDidMount: function() {
    this.loadLikeFromServer();
  },
  
  handleClick: function( event ){
    var liked = !this.state.liked;

    /*Update server info here */
    this.handleLikeSubmit({liked: liked});
  },

  render: function() {
    
    var likeOrNot = this.state.liked ? 'UnLike' : 'Like';
    
    return (
        /* It says its better to return null as reactjs will remove this from DOM, which is more effeciency */
        React.createElement("span", null, 
           this.state.likecount ?
          React.createElement("span", {id: "likewidget", className: "DisplayStyle", className: "likeWidget"}, 
              React.createElement("a", null, this.state.likecount), " ·"
          )  : null, 
          React.createElement("a", {onClick: this.handleClick, className: "cvoter"}, likeOrNot)
        )
    );
  }
});

var ReplyButton = React.createClass({displayName: "ReplyButton",
  
  handleClick: function( event ){
  },

  render: function() {

    return (
      React.createElement("a", {onClick: this.handleClick, className: "j-write-reply", href: "#", "data-parent-id": "event_comment-450097011"}, "Reply") 
    );
  }
});

var DeleteMark = React.createClass({displayName: "DeleteMark",
  render: function() {

    return (
      React.createElement("div", {className: "x-mark-cont clearfix"}, 
          React.createElement("div", {className: "x-mark"})
      ) 
    );
  }

});

var DeleteButton = React.createClass({displayName: "DeleteButton",


  handleClick: function( event ){

    event.preventDefault();
    /* Remove the comment delete from DOM */
    /* Delete option to server */
  },

  render: function() {

    return (
      React.createElement("ul", {className: "resetList x-menu theme-bgcolor--actionlist theme-color--actionlist"}, 
        React.createElement("li", null, React.createElement("a", {href: "#", onClick: this.handleClick, className: "deleter", "data-id": "450097011"}, "Delete"))
      ) 
    );
  }
});

var MidDot = React.createClass({displayName: "MidDot",

  render: function() {

    return (
      React.createElement("b", null, "  ·  ")
    );
  }
});

var commentNode = React.render(
React.createElement(CommentBox, {url: urlPrefix, pollInterval: 2000}),
  document.getElementById('event-comments-section')

);

$('#event-comments-section').bind('login', function(event, loginUser){
  user = loginUser;
  userlogin=true;
  if(commentNode){
    commentNode.forceUpdate();
  }
});

