'use strict';
import React from 'react';
import { connect } from 'react-redux';
import { BASE_URL } from 'config';
import SimditorTextarea from 'components/simditor';
import { groupActions } from 'core/group';
import Crop from 'components/crop';
var $ = require('jquery');

class FormGroup extends React.Component {
  render() {

    const {
      action,
      existedGroups
    } = this.props;

    if(action === 'new') {

      var optionarr = existedGroups.map(function(group) {
        return(
          <option value = {group.id} key = {group.id}> {group.name} </option>
        )
      })
      return(
        <div className="form-group form-group-lg">
            <label htmlFor="fatherGroup">Belong to:</label>
            <select id="fatherGroup" className="form-control">
              <option value='0'>Independent(default)</option>
                {optionarr}
            </select>
        </div>
      )
    } else {
      return(<div></div>)
    }
  }
}

class GroupMgr extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      targetgroup: {},
      cropdata: null
    }
  }

  getgroup(allGroups, gid) {

    var groupid = (gid > 0) ? gid : 0;

    //console.log("target group id is:"+groupid);      

    var that = this;

    //get corresponding group name        
    $.each(allGroups, function(i, group) {
      var g = Object.assign({}, group);
      var id = group.id;

      if(id == groupid) {
        that.setState({ targetgroup: g });

        return false;
      }
    });
  }

  componentDidMount() {
    const {
      params,
      existedGroups
    } = this.props;

    if((params.oprTag == 'edit') && (!this.state.targetgroup.id) && (existedGroups.length > 0)) { //parse the desired group info from redux store
      this.getgroup(existedGroups, params.groupId);
    }
  }

  componentWillReceiveProps(nextProps) {
    if((nextProps.existedGroups.length > 0) && (this.props.existedGroups.length == 0)) {
      this.getgroup(nextProps.existedGroups, this.props.params.groupId);
    }

    if((nextProps.params.oprTag == 'edit') && (this.state.targetgroup.id) && (nextProps.params.groupId != this.state.targetgroup.id)) {
      //console.log("group id changed");  
      this.getgroup(this.props.existedGroups, nextProps.params.groupId);
    }

  }

  loadDesc() {
    const {
      params
    } = this.props;

    if((params.oprTag == 'edit') && (this.state.targetgroup.id)) { //redux store parameters are ready

      return(
        <SimditorTextarea
          id='rteditor'
          value = {this.state.targetgroup.desc}  
          onChange = {this.updateEditContent}          
        />
      )
    } else if((params.oprTag == 'edit') && (!this.state.targetgroup.id)) { //redux store parameters are not ready, or it store parameters are ready but desired group info haven't been parsed

      return(
        <div> <h4>Loading...</h4></div>
      )
    } else if(params.oprTag == 'new') {
      return(
        <SimditorTextarea
          id='rteditor'
          value = ''       
          onChange = {this.updateEditContent}
        />
      )
    }
  }

  updateEditContent = (value) => {
    document.getElementById("hiddeneditor").innerHtml = value;
  }

  handlechange = (e) => {
    var group = Object.assign({}, this.state.targetgroup, { name: e.target.value });
    //group.name = e.target.value;
    this.setState({ targetgroup: group });
  }

  formsubmit = (form) => {
    const {
      auth,
      existedGroups
    } = this.props;

    form.preventDefault();

    if(!auth.authenticated) {
      alert("You need to sign in before submitting the data");
      return false;
    }

    var action = document.getElementById("action").value;
    var actionUrl = document.getElementById("actionUrl").value;

    var data = {};

    data.Name = $('#inputName').val();
    data.Desc = document.getElementById("hiddeneditor").innerHtml;

    if(this.state.cropdata) {
      data.Pic = this.state.cropdata;
      if(!data.Pic) {
        alert('Please crop image before submit ^_^');
        return;
      }
      var picDataLen = data.Pic.length;
      if(picDataLen > 1048576) {
        alert('Image size exceeds 1M. Current cropped size is:' + Math.round(picDataLen / 1000) + 'k');
        return;
      }

    }

    if(action === 'new') {
      data.Father = $('#fatherGroup').val();
      var redirectUrl = this.props.createGroup(data);

      if(redirectUrl.length > 0) {
        if(confirm("Operation Succeeded. Do you want to redirect to the home page of this group?")) {
          location.href = redirectUrl;
        }
      }
    }

    //if the action is to edit group, then need append group id
    if(action === 'edit') {
      data.id = $('#groupID').val();
      //actionUrl = actionUrl+$('#groupID').val();
      var redirectUrl = this.props.updateGroup(data);

      //console.log("redirectUrl:"+redirectUrl);

      if(redirectUrl.length > 0) {
        if(confirm("Operation Succeeded. Do you want to redirect to the home page of this group?")) {
          location.href = redirectUrl;
        }
      }
    }
  }

  getCropData = (data) => {
    this.setState({
      cropdata: data
    })
  }

  render() {

    const {
      existedGroups,
      params
    } = this.props;

    var action = params ? params.oprTag : 'new';

    //console.log("this.state.targetgroup.name is"+this.state.targetgroup.name);

    switch(action) {
      case 'new':
        var groupTitle = 'New Group';
        var actionUrl = BASE_URL + 'newGroup';
        break;
      case 'edit':
        var groupTitle = 'Edit Group';
        var actionUrl = BASE_URL + 'editGroup/' + params.groupId;
        break;
      default:
        var groupTitle = 'Unknown Title';
    }

    var groupid = params ? params.groupId : '0';

    if(groupid == 0) {
      <div><h4>Invalid Group Id. Please check URL link. </h4></div>
    } else {
      return(
        <div className="row" style={{marginTop:"80px"}}>
                          
        <div className="col-md-10 col-md-offset-1">
          <div className="panel panel-default">
            <div className="panel-className">
              <div className="page-header">
                <h1>{groupTitle}</h1>
              </div>
              <form encType="multipart/form-data" method="post" onSubmit={this.formsubmit.bind(this)} id="GroupForm1" >
                  <input id="action" type="hidden" value={action} />
                  <input id="actionUrl" type="hidden" value={actionUrl} />
                  <div className="form-group form-group-lg">
                      <label htmlFor="inputName">Name</label>
                      <input type="text" className="form-control" id="inputName" name= "Name" placeholder="Group name" required="required" value = {this.state.targetgroup.name?this.state.targetgroup.name:''} onChange = {this.handlechange}/>
                      <input id="groupID" type="hidden" value= { !this.state.targetgroup.id? '' : this.state.targetgroup.id} />
                  </div>
                  <FormGroup
                    action = {action}
                    existedGroups = {existedGroups}
                  />
                  <div className="form-group">
                    <label htmlFor="inputDesc">Group description</label>
                    <div id="group-desc">
                      {this.loadDesc()}
                    </div>   
                    <textarea id="hiddeneditor" style={{display:"none"}}></textarea>                    
                  </div>         
                  
                  <div className="form-group form-group-lg">
                    <label>Group picture </label>
                    <p className="help-block">Please replace the default image with your own one and crop the image</p>
                  </div>                  
                  <Crop
                    informCropData = {this.getCropData.bind(this)}
                  />
                  
                  <div className="form-group form-group-lg">
                    <button id="submit_btn" type="submit" className="btn btn-primary btn-lg" autoComplete="off">Publish</button>
                  </div>                  
              </form>
            </div>
            </div>
          </div>
        </div>
      )
    }
  }
}

export default connect((state, ownProps) => ({
  existedGroups: state.group.allGroups,
  auth: state.auth
}), groupActions)(GroupMgr)