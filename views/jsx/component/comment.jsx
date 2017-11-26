var React = require('react');
var CommentBox = React.createClass({

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
    console.log('component Didmount');
    this.loadCommentsFromServer();
    //setInterval( this.loadCommentsFromServer, this.props.pollInterval);
  },

  render: function(){

    return (
      <div >
        <CommentHeader/>
        { userlogin ? <CommentForm onCommentSubmit={this.handleCommentSubmit }/> : null }
        <CommentList onCommentSubmit={this.handleCommentSubmit} onCommentDelete={this.handleCommentDelete} data={this.state.data} filter={this.state.filter} />
      </div>
    );
  }
});

var CommentHeader = React.createClass({
  render: function(){
    var commentHeader;

    if( !userlogin ){
    commentHeader =  <p id="commentsPostExplain"><a href='#loginModal' data-toggle="modal" data-backdrop="static"> Login </a> to comment</p> ;
    }else{
    var greeting = "Hey, " + user.fullname + ", Join the conversation";
    commentHeader = <h4 className="talk-heading margin-bottom">{greeting}</h4> ;
    }

    return ( 
    <div>
    { commentHeader }
    </div>
    );
  }
});

var CommentList = React.createClass({

  render: function(){      
    var onCommentSubmit = this.props.onCommentSubmit;
    var onCommentDelete = this.props.onCommentDelete;

    var commentNodes = this.props.data.map( function ( comment ){
        return ( 
        <CommentReply key={comment.id} url={urlPrefix} comment={comment} onCommentSubmit={onCommentSubmit} onCommentDelete={onCommentDelete}/>
        );
     
    });

    return (
      <ul className="resetList dividedList comments">
        {commentNodes}
      </ul>
    );
  }
});    

var CommentReply = React.createClass({
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
        <ul>
        <Comment comment={comment} onClickReplyButton={showReplyForm} onDeleteSubmit={this.props.onCommentDelete}/>
        <ReplyList replyinfo={replyto} replyFormVisible={replyFormVisible} onClickReplyButton={showReplyForm} url={replyUrl} commentID={comment.id} />
        </ul>
    );
  }
});    

var CommentForm = React.createClass({
  
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
        <div className="figureset new-comment">
          <UserFigure user={user}/>
          <div className="figureset-description">
            <div className="comment-wrap"> 
              <div className="comment-input-wrap"> 
                <textarea name="newComment" className="j-comment-input J_onClick textInputTip span-100 hasMaxLen maxChars1000" title="Ask a question, share something, or leave a comment..." placeholder="Ask a question, share something, or leave a comment..." ref="text"></textarea> 
                 <div className="nib">
                     <div className="inner-nib"></div>
                 </div> 
              </div>
            </div>
            <div className="comment-actions">
                <button onClick={this.handleSubmit} className="j-submit-comment button primary small">Post</button> 
            </div>
          </div>
        </div>
    );
  }
});    

var Comment = React.createClass({

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
      <li>
        <div className="figureset">
          <UserFigure user={this.props.comment.createdby}/>
          <div className="figureset-description">
            <h5>
            <UserName user={this.props.comment.createdby}/>
            {this.props.comment.maincomment && this.props.replytoUser ?" to ": null } 
            {this.props.comment.maincomment && this.props.replytoUser ? <UserName user={this.props.replytoUser}/>: null } 
            </h5>
            <div className="comment-body"> <p>{this.props.comment.content}</p></div>
            <p>
            { userlogin ? 
            <LikeWidget url={url} commentid={this.props.comment.id}/> 
            : null }  
            { userlogin ?  <MidDot/> : null }  
            { userlogin ? 
            <a onClick={this.handleReplyButton} className="j-write-reply" href={this.replyButtonHref} data-parent-id="event_comment-450097011">Reply</a> 
            : null }  
            { userlogin ?  <MidDot/> : null }  
              {commentDate4Show}
            </p>
          </div>
          { userlogin && this.props.comment.createdby.id == user.id ? 
          <div className="x-mark-cont clearfix" onMouseOver={this.showDelete} onMouseOut ={this.hideDelete}>    
              <div  className={this.state.markhover? "x-mark hoverintent" : "x-mark"} ></div>
          </div> 
          : null }
          { userlogin && this.props.comment.createdby.id == user.id ? 
          <ul className={this.state.markhover? "resetList x-menu hoverintent" : "resetList x-menu"} onMouseOver={this.showDelete} onMouseOut={this.hideDelete}>    
            <li><a href="#" onClick={this.handleDeleteClick} className="deleter" >Delete</a></li>  
          </ul> 
          : null }
        </div>
      </li>
    );
  }
});

var ReplyList = React.createClass({

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
      <Comment key={reply.id} comment={reply} onClickReplyButton={onClickReplyButton} onDeleteSubmit = {onDeleteSubmit} replytoUser={replyUserName }/>
      );
    });

    return (
      <li className="replies">
        <ul id={this.replyID} className="dividedList tight">
            { this.state.replies.length > 2 && !this.state.showall ? <li><div  className="small leading-bottom"><a href={this.replyIDHref} onClick={this.showAllReplies} className="j-show-all-replies">View all { this.state.replies.length } replies</a></div></li> : null }
          { this.state.replies.length ? {replyNode} : null }
          { this.props.replyFormVisible ? <ReplyForm onReplySubmit={this.handleReplySubmit} replyinfo={this.props.replyinfo} commentID={this.props.commentID}/>  : null }
        </ul>
      </li>
    );
  }
});

var ReplyForm = React.createClass({
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
      <li id={id} className="reply-wrap">
        <textarea onKeyPress={this.replySubmit} ref="replytext" aria-describedby="enterDescribe" className="reply-input textInputTip" title="Write a reply..."></textarea>
        <div className="dot-loader-16 invisible"></div>
      </li>
    );
  }
});

var UserFigure = React.createClass({
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
      <div className="figureset-figure">
          <a href="/user/myprofile" className="mem-photo-background-60 square-50" style={imgStyle} ></a>
      </div>
    );
  }

});

var UserName = React.createClass({
  render: function() {

    return (
      <a href="/user/myprofile" className="memberinfo-widget" data-memberid={this.props.user.id} title={this.props.user.fullname}>{this.props.user.fullname}</a>
    );
  }

});

var LikeWidget = React.createClass({

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
        <span>
          { this.state.likecount ?
          <span id="likewidget" className="DisplayStyle"className="likeWidget">
              <a >{this.state.likecount}</a> &middot;
          </span>  : null }
          <a onClick={this.handleClick} className="cvoter">{likeOrNot}</a>
        </span>
    );
  }
});

var ReplyButton = React.createClass({
  
  handleClick: function( event ){
  },

  render: function() {

    return (
      <a onClick={this.handleClick} className="j-write-reply" href="#" data-parent-id="event_comment-450097011">Reply</a> 
    );
  }
});

var DeleteMark = React.createClass({
  render: function() {

    return (
      <div className="x-mark-cont clearfix">    
          <div className="x-mark"></div>  
      </div> 
    );
  }

});

var DeleteButton = React.createClass({


  handleClick: function( event ){

    event.preventDefault();
    /* Remove the comment delete from DOM */
    /* Delete option to server */
  },

  render: function() {

    return (
      <ul className="resetList x-menu theme-bgcolor--actionlist theme-color--actionlist">    
        <li><a href="#" onClick={this.handleClick} className="deleter" data-id="450097011" >Delete</a></li>  
      </ul> 
    );
  }
});

var MidDot = React.createClass({

  render: function() {

    return (
      <b>  &middot;  </b>
    );
  }
});

var commentNode = React.render(
<CommentBox url={urlPrefix} pollInterval={2000}/>,
  document.getElementById('event-comments-section')

);

$('#event-comments-section').bind('login', function(event, loginUser){
  user = loginUser;
  userlogin=true;
  if(commentNode){
    commentNode.forceUpdate();
  }
});

