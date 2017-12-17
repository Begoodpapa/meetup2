import {
  GROUP_CREATE_SUCCESS,
  GROUPS_READ_SUCCESS,
  GROUP_UPDATE_SUCCESS
} from './action-types';

var _ = require('lodash');
var $ = require("jquery");

export const initialState = {

  allGroups: [],
  hottestGroups: [],
  latestGroups: []

}

function updateAll(allGroups, targetGroup) {
  var groups = _.clone(allGroups);

  $.each(allGroups, function(key, value) {
    if(value.id == targetGroup.id) {
      groups[key].desc = targetGroup.Desc;
      groups[key].name = targetGroup.Name;
      //TODO: update groupfd later
      return false;
    }
  })

  return groups;

}

function updateHottest(hottestGroups, targetGroup) {
  var groups = _.clone(hottestGroups);

  $.each(hottestGroups, function(key, value) {
    if(value.id == targetGroup.id) {
      groups[key] = targetGroup;
      return false;
    }
  })

  return groups;

}

function updateLatest(latestGroups, targetGroup) {
  var groups = _.clone(latestGroups);

  $.each(latestGroups, function(key, value) {

    if(value.id == targetGroup.id) {
      groups[key].desc = targetGroup.Desc;
      groups[key].name = targetGroup.Name;
      //TODO: update groupfd later

      return false;;
    }
  })

  return groups;
}

export function groupReducer(state = initialState, action) {

  switch(action.type) {
    case GROUP_CREATE_SUCCESS:
      return state; //no need to update redux store because readGroups() will be invoked right after creation.

    case GROUPS_READ_SUCCESS:
      return Object.assign({}, state, { allGroups: action.payload.allgroups }, { hottestGroups: action.payload.hottestGroups }, { latestGroups: action.payload.latestGroups });

    case GROUP_UPDATE_SUCCESS:
      var newAllGroups = updateAll(state.allGroups, action.payload);
      var newHottestGroups = updateHottest(state.hottestGroups, action.payload);
      var newLatestGroups = updateLatest(state.latestGroups, action.payload);

      return Object.assign({}, state, { allGroups: newAllGroups }, { hottestGroups: newHottestGroups }, { latestGroups: newLatestGroups });

    default:
      return state
  }

}