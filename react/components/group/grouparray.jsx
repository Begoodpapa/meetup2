'use strict';
import React from 'react';
import { connect } from 'react-redux';
import { BASE_URL } from 'config';

class GroupArr extends React.Component {

  formgroups(grouparr) {

    var returnarr = grouparr.map(function(item, index) {

      const groupfd = BASE_URL + item.groupfd;
      const groupid = item.id;
      const groupname = item.name;

      //console.log("groupname:"+item.name);    

      return(
        <div className= "col-sm-6 col-md-4" key={groupid}> 
          <div className="thumbnail" style={{minHeight:"430px"}}>
            <a href= {'#/group/show/' + groupid + '/overview'}>
              <h3> {groupname} </h3> 
              <img style={{width:'100%', height:'300px'}} src= {groupfd} />
              <p>{item.userIds.length} members</p>
            </a>
          </div> 
        </div>)
    })
    return returnarr;
  }

  //search result of querying by groupid or text that typed in search window. 
  searchgroups(id, str) {
    const {
      allgroups
    } = this.props;

    var returnarr = [];

    allgroups.map(function(item, index) {
      const groupid = item.id;
      const groupname = item.name;

      const lcGroupName = groupname.toLowerCase(); //lower case group name
      const lcStr = str.toLowerCase();

      if((groupid == id) || (lcGroupName.indexOf(lcStr) >= 0)) {
        const groupfd = BASE_URL + item.groupfd;

        returnarr.push(
          <div className= "col-sm-6 col-md-4" key={groupid}> 
            <div className="thumbnail" style={{minHeight:"430px"}}>
              <a href= {'#/group/show/' + groupid + '/overview'}>
                <h3> {groupname} </h3> 
                <img style={{width:'100%', height:'300px'}} src= {groupfd} />
                <p>{item.user.length} members</p>
              </a>
            </div> 
          </div>)
      }
    })
    return returnarr;
  }

  render() {
    const {
      hottestgroups,
      latestgroups,
      allgroups,
      type, //type is either of [hottest, latest, all, search]
      searchid,
      searchstr
    } = this.props;

    var grouparr = '';

    switch(type) {
      case 'hottest':
        grouparr = this.formgroups(hottestgroups);
        break;
      case 'latest':
        grouparr = this.formgroups(latestgroups);
        break;
      case 'all':
        grouparr = this.formgroups(allgroups);
        break;
      case 'search':
        grouparr = this.searchgroups(searchid, searchstr);
        break;
    }
    return(
      <div>
        {grouparr}
      </div>
    )
  }
}

export default connect((state, ownProps) => ({
  hottestgroups: state.group.hottestGroups,
  latestgroups: state.group.latestGroups,
  allgroups: state.group.allGroups
}))(GroupArr)