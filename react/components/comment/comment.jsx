var $= require('jquery');
import React from 'react';
import ReactDOM from 'react-dom';
import {BASE_URL} from 'config';

class CommentBox extends React.Component{

  loadCommentsFromServer() {
    $.ajax({
      url: this.props.baseUrl+this.props.urlPrefix,
      dataType: 'json',
      data:{category:this.props.category, relevantid: this.props.relevantid},
      success: function( data ){
        this.setState({data: JSON.parse(data)});
      }.bind( this ),
      error: function( xhr, status, err ){
        console.error( this.props.url, status, err.toString());
      }.bind( this )
    });
  }
 
  handleCommentSubmit(comment){
    //Submit to server and refresh the list
    var comments = this.state.data;
    Object.assign(comment, {category: this.props.category, relevantid: this.props.relevantid});

    $.ajax({
      url: this.props.baseUrl+this.props.urlPrefix,
      dataType: 'json',
      type: 'POST',
      data: comment,
      success: function(data) {      	
      	if (data.error){      	  
      	  alert(data.error);
      	}
      	else{
	        comments.unshift(JSON.parse(data));
	        this.setState({data: comments});
        }
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());        
      }.bind(this)
    });
  }

  handleCommentDelete(commentid){
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
      url: this.props.baseUrl + this.props.urlPrefix + '/' + commentid + '/delete',
      dataType: 'json',
      type: 'POST',
      success: function(data) {
        this.setState({data: newComments});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  }

  constructor(props){
    super(props);
    this.state={data: []};
  }

  componentDidMount(){
    this.loadCommentsFromServer();
  }

  render(){

    var baseUrl= this.props.baseUrl;
    var urlPrefix = this.props.urlPrefix;

    return (
      <div >
        <CommentHeader user={this.props.auth} />
        { this.props.auth.authenticated ? <CommentForm user={this.props.auth} onCommentSubmit={this.handleCommentSubmit.bind(this) }/>: null}
        <CommentList user={this.props.auth} baseUrl={baseUrl} urlPrefix={urlPrefix} onCommentSubmit={this.handleCommentSubmit} onCommentDelete={this.handleCommentDelete.bind(this)} data={this.state.data} filter={this.state.filter} />
      </div>
    );
  }
}

class CommentHeader extends React.Component{
  render(){
    var commentHeader;
    var user = this.props.user;
    
    if( user&&user.authenticated ){
      var greeting = "Hey, " + user.user.fullname + ", Join the conversation";
      commentHeader = <h4 className="talk-heading margin-bottom">{greeting}</h4> ;
    }else{
      commentHeader = <h4><p id="commentsPostExplain">You can login to give comments</p></h4> ;
    }

    return ( 
    <div>
    <p/>
    { commentHeader }
    </div>
    );
  }
}

class CommentList extends React.Component{

  render(){      
    var onCommentSubmit = this.props.onCommentSubmit;
    var onCommentDelete = this.props.onCommentDelete;
    var user = this.props.user;
    var baseUrl = this.props.baseUrl;
    var urlPrefix = this.props.urlPrefix;

    var commentNodes = this.props.data.map( function ( comment ){
        return ( 
        <CommentReply user={user} key={comment.id} baseUrl={baseUrl} urlPrefix={urlPrefix} comment={comment} onCommentSubmit={onCommentSubmit} onCommentDelete={onCommentDelete}/>
        );
     
    });

    return (
      <ul className="resetList dividedList comments">
        {commentNodes}
      </ul>
    );
  }
}

class CommentReply extends React.Component{
  
  constructor(props){ 
    super(props); 
    this.state={ replyFormVisible: false,
               replyinfo: {replytoid: 0, maincommentid:0}
             };
  }
  

  showReplyForm(replyinfo){
      this.setState({ replyFormVisible: true, replyinfo: replyinfo });
  }

  render(){      

    var showReplyForm = this.showReplyForm;
    var comment = this.props.comment;
    var replyto = this.state.replyinfo;
    var replyFormVisible = this.state.replyFormVisible;
    var replyUrl = this.props.baseUrl + this.props.urlPrefix + comment.id + "/replies";
    var baseUrl = this.props.baseUrl;
    var urlPrefix = this.props.urlPrefix;

    return (
        <ul>
        <Comment user={this.props.user} comment={comment} baseUrl={baseUrl} urlPrefix={urlPrefix} onClickReplyButton={showReplyForm.bind(this)} onDeleteSubmit={this.props.onCommentDelete}/>
        <ReplyList user={this.props.user} baseUrl={baseUrl} urlPrefix={urlPrefix} replyinfo={replyto} replyFormVisible={replyFormVisible} onClickReplyButton={showReplyForm.bind(this)} commentID={comment.id} />
        </ul>
    );
  }
}    

class CommentForm extends React.Component{

  constructor(props){ 
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this); 
  }

  handleSubmit( e ){
    e.preventDefault();
    var text = this.refs.text.value.trim();

    if( !text ){
      return;
    }
   
    // Send request to server
    this.props.onCommentSubmit({content: text, replyto: 0, maincomment: 0 });

    this.refs.text.value = '';
    return;
  }

  render(){
    return (
        <div className="figureset new-comment">
          <UserFigure user={this.props.user}/>
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
}    

class Comment extends React.Component{

  constructor(props){
    super(props);
    this.state = {markhover: false}
  }

  handleReplyButton(event){
    var replytoid = this.props.comment.id;
    var maincommentid = this.props.comment.id;

    if( this.props.comment.maincomment != 0 ){
      maincommentid = this.props.comment.maincomment;
    }

    this.props.onClickReplyButton( { replytoid: replytoid, maincommentid: maincommentid });
  }


  handleDeleteClick( event ){

    /*Update server info here */
    this.props.onDeleteSubmit(this.props.comment.id);
  }

  showDelete( event ){
    this.setState({markhover: true });
  }
  
  hideDelete(event){
    this.setState({markhover: false });
  }

  render(){

    var monthArray = [ "Jan", "Feb", "Mar", "Apr", "May" , "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    var commentDate = new Date( this.props.comment.createdAt);
    var curDate = new Date();
    var commentDate4Show = monthArray[commentDate.getMonth()];
    var url = this.props.baseUrl + this.props.urlPrefix + '/' + this.props.comment.id + "/like";
    var commentID = this.props.comment.maincommentid ? this.props.comment.maincommentid : this.props.comment.id;
    var replyButtonHref = "#reply-form-to-" + commentID;
    var user = this.props.user;
    var userlogin = user.authenticated;

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
            <a onClick={this.handleReplyButton.bind(this)} className="j-write-reply" href={this.replyButtonHref} data-parent-id="event_comment-450097011">Reply</a> 
            : null }  
            { userlogin ?  <MidDot/> : null }  
              {commentDate4Show}
            </p>
          </div>
          { userlogin && this.props.comment.createdby.id == user.id ? 
          <div className="x-mark-cont clearfix" onMouseOver={this.showDelete.bind(this)} onMouseOut ={this.hideDelete.bind(this)}>    
              <div  className={this.state.markhover? "x-mark hoverintent" : "x-mark"} ></div>
          </div> 
          : null }
          { userlogin && this.props.comment.createdby.id == user.id ? 
          <ul className={this.state.markhover? "resetList x-menu hoverintent" : "resetList x-menu"} onMouseOver={this.showDelete.bind(this)} onMouseOut={this.hideDelete.bind(this)}>    
            <li><a href="#" onClick={this.handleDeleteClick.bind(this)} className="deleter" >Delete</a></li>  
          </ul> 
          : null }
        </div>
      </li>
    );
  }
}

class ReplyList extends React.Component{

  constructor(props){
    super(props);
    this.state = {
      replies: [],
      showall: false}
  }

  loadRepliesFromServer() {
    $.ajax({
      url: this.props.baseUrl + this.props.urlPrefix + '/' + this.props.commentID + "/replies",
      dataType: 'json',
      success: function( data ){
        this.setState({replies: JSON.parse(data)});
      }.bind( this ),
      error: function( xhr, status, err ){
        console.error( this.props.baseUrl + this.props.urlPrefix, status, err.toString());
      }.bind( this )
    });
  }

  componentDidMount() {
    this.loadRepliesFromServer();
  }

  handleReplySubmit( reply ){
    //Submit to server and refresh the list
    var replies = this.state.replies;

    $.ajax({
      url: this.props.baseUrl + this.props.urlPrefix,
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
  }

  handleReplyDelete( replyid ){
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
      url: this.props.baseUrl + this.props.urlPrefix + '/' + replyid + '/delete',
      dataType: 'json',
      success: function(data) {
        this.setState({replies: newReplies});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  }


  showAllReplies( event ){
    this.setState({showall: true});
  }

  findReplytoUser( replyid , replyIndex ){
    var i = replyIndex > this.state.replies.length  - 1? this.state.replies.length  -1  : replyIndex;

    for( ; i >= 0; i--){
      if( this.state.replies[i].id == replyid ){
        return this.state.replies[i].createdby;
      }
    }
    return "";
  }

  render(){
    var onClickReplyButton = this.props.onClickReplyButton;
    var onDeleteSubmit = this.handleReplyDelete;
    var findReplytoUser= this.findReplytoUser.bind(this);
    var filter = this.props.filter;
    var showcount = 0;
    var showall = this.state.showall;
    var replyID = "replyto-" + this.props.commentID;
    var replyIDHref = "#" + replyID;
    var baseUrl = this.props.baseUrl;
    var urlPrefix = this.props.urlPrefix;

    var replies = this.state.replies;
    var user = this.props.user;

    var replyNode = replies.map( function ( reply ){
      if( !showall && showcount >= 2){
        return null;
      }
      var replyUserName = findReplytoUser( reply.replyto.id, showcount - 1);
      showcount += 1;
      return ( 
      <Comment key={reply.id} baseUrl={baseUrl} urlPrefix={urlPrefix} user={user} comment={reply} onClickReplyButton={onClickReplyButton.bind(this)} onDeleteSubmit = {onDeleteSubmit.bind(this)} replytoUser={replyUserName}/>
      );
    });

    return (
      <li className="replies">
        <ul id={this.replyID} className="dividedList tight">
            { this.state.replies.length > 2 && !this.state.showall ? <li><div  className="small leading-bottom"><a href={this.replyIDHref} onClick={this.showAllReplies.bind(this)} className="j-show-all-replies">View all { this.state.replies.length } replies</a></div></li> : null }
          { this.state.replies.length ? replyNode : null }
          { this.props.replyFormVisible ? <ReplyForm onReplySubmit={this.handleReplySubmit.bind(this)} replyinfo={this.props.replyinfo} commentID={this.props.commentID}/>  : null }
        </ul>
      </li>
    );
  }
}

class ReplyForm extends React.Component{
  componentDidMount(){
      this.refs.replytext.focus();
  }

  componentDidUpdate(){
      this.refs.replytext.focus();
  }
  

  replySubmit( e ){
    var ENTER = 13;
    if( e.keyCode == ENTER || e.which == ENTER ){
      var reply = new Object();
      var text = this.refs.replytext.value.trim();

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

      this.refs.replytext.value = '';
    }
    return;
  }

  render(){
   
    var id = "reply-form-to-"+ this.props.commentID;
    return (
      <li id={id} className="reply-wrap">
        <textarea onKeyPress={this.replySubmit.bind(this)} ref="replytext" aria-describedby="enterDescribe" className="reply-input textInputTip" title="Write a reply..."></textarea>
        <div className="dot-loader-16 invisible"></div>
      </li>
    );
  }
}

class UserFigure extends React.Component{
  render() {
    if(!this.props.user){
      return (
        <div className="figureset-figure">
        </div>
      )
    }
    var userfd = this.props.user.userfd;

    if( !userfd ){
       userfd = BASE_URL + "/images/default_upp.jpg";
    }
    var imgStyle = {
      color: 'green',
      display: 'block',
      backgroundImage: 'url(' + userfd + ')'
    };
    return (
      <div className="figureset-figure">
          <a href={"#/showuserprofile/"+this.props.user.id+"/"} className="mem-photo-background-60 square-50" style={imgStyle} ></a>
      </div>
    );
  }

}

class UserName extends React.Component{
  render() {

    return (
      <a href={"#/showuserprofile/"+this.props.user.id+"/"} className="memberinfo-widget" data-memberid={this.props.user.id} title={this.props.user.fullname}>{this.props.user.fullname}</a>
    );
  }

}

class LikeWidget extends React.Component{

  constructor(props){
    super(props);
    this.state = {
      liked: false,
          likecount:0}
  }

  loadLikeFromServer() {
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
  }
 
  handleLikeSubmit( likedata ){
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
  }

  componentDidMount() {
    this.loadLikeFromServer();
  }
  
  handleClick( event ){
    var liked = !this.state.liked;

    /*Update server info here */
    this.handleLikeSubmit({liked: liked, commentid: this.props.commentid});
  }

  render() {
    
    var likeOrNot = this.state.liked ? 'UnLike' : 'Like';
    
    return (
        /* It says its better to return null as reactjs will remove this from DOM, which is more effeciency */
        <span>
          { this.state.likecount ?
          <span id="likewidget" className="DisplayStyle"className="likeWidget">
              <a >{this.state.likecount}</a> &middot;
          </span>  : null }
          <a onClick={this.handleClick.bind(this)} className="cvoter">{likeOrNot}</a>
        </span>
    );
  }
}

class ReplyButton extends React.Component{
  
  handleClick( event ){
  }

  render() {

    return (
      <a onClick={this.handleClick} className="j-write-reply" href="#" data-parent-id="event_comment-450097011">Reply</a> 
    );
  }
}

class DeleteMark extends React.Component{
  render() {

    return (
      <div className="x-mark-cont clearfix">    
          <div className="x-mark"></div>  
      </div> 
    );
  }

}

class DeleteButton extends React.Component{


  handleClick( event ){

    event.preventDefault();
    /* Remove the comment delete from DOM */
    /* Delete option to server */
  }

  render() {

    return (
      <ul className="resetList x-menu theme-bgcolor--actionlist theme-color--actionlist">    
        <li><a href="#" onClick={this.handleClick} className="deleter" data-id="450097011" >Delete</a></li>  
      </ul> 
    );
  }
}

class MidDot extends React.Component{

  render() {

    return (
      <b>  &middot;  </b>
    );
  }
}

export default CommentBox
