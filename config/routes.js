'use strict';

module.exports.routes = {

/*
  '/': {
    'controller': 'Home',
    'action': 'index'
  },
*/

/*
  'GET /': {
    view: "index",
    locals: {
        layout: null
    }
  },
  */
  
'GET /': {
    view: "homepage",
    locals: {
        layout: null
    }
  }, 

'GET /episode1': {
    view: "episode1",
    locals: {
        layout: null
    }
 }, 

'GET /episode2': {
    view: "episode2",
    locals: {
        layout: null
    }
  },   
  
'GET /episode3': {
    view: "episode3",
    locals: {
        layout: null
    }
 },    

'GET /episode4': {
    view: "episode4",
    locals: {
        layout: null
    }
  },   

'GET /episode5': {
    view: "episode5",
    locals: {
        layout: null
    }
  },   

'GET /episode6': {
    view: "episode6",
    locals: {
        layout: null
    }
  },   
  
'GET /certificate': {
    view: "cert",
    locals: {
        layout: null
    }
 }, 
  
'GET /letters': {
    view: "letters",
    locals: {
        layout: null
    }
  },   
  
'GET /beehive': {
    view: "index",
    locals: {
        layout: null
    }
  },  

  '/sview': {
    view: 'sEvent'
  },

  'get /chat': {
    controller: 'Chat',
    action: 'get'
  },

  'post /chat': {
    controller: 'Chat',
    action: 'post'
  },

  'GET /login': {
    controller: 'Landing',
    action: 'login',
    locals: {
      layout: 'layout_login'
    }
  },

  'POST /auth/login': { // this is bypassed by assets/js/common/login_modal.js calling from views/component/navbar2.ejs
    'controller': 'Auth',
    'action': 'login'
  },

  'POST /auth/loginAjax': {
    'controller': 'Auth',
    'action': 'loginAjax'
  },

  '/calender': {
    'controller': 'Home',
    'action': 'calender'
  },

  'GET /group/:gid/event/:eid/show': {
    controller: 'Event',
    action: 'showAjax'
  },

  'GET /group/:gid/newEvent': {
    controller: 'Event',
    action: 'create'
  },

  'POST /group/:gid/newEvent': {
    controller: 'Event',
    action: 'doCreate'
  },

  'GET /group/:gid/event/:eid/edit': {
    controller: 'Event',
    action: 'edit'
  },

  'POST /group/:gid/event/:eid/eventDoEdit': {
    controller: 'Event',
    action: 'doEdit'
  },

  '/group/:gid/event/:eid/publish': {
    controller: 'Event',
    action: 'publish'
  },

  'POST /group/:gid/album/:eid/editPicDesc': {
    controller: 'Event',
    action: 'editPicDesc'
  },

  '/event/imageupload': {
    'controller': 'Event',
    'action': 'imageUpload'
  },

  'POST /event/joinevent/:id': {
    'controller': 'Event',
    'action': 'addUserToEvent'
  },

  'POST /event/leftevent/:id': {
    'controller': 'Event',
    'action': 'removeUserFromEvent'
  },

  '/user/myevent': {
    'controller': 'User',
    'action': 'showMyEvent'
  },

  '/user/mygroup': {
    'controller': 'User',
    'action': 'showMyGroup'
  },


  'GET /user/myprofile': {
    controller: 'User',
    action: 'showMyProfile'
  },

  'GET /user/:uid/profile': {
    controller: 'User',
    action: 'showProfile'
  },


  'POST /mailhook': {
    'controller': 'Mailhook',
    'action': 'hook'
  },

  'GET /api/group': {
    'controller': 'Group',
    'action': 'find'
  },

  'GET /group/show/:id': {
    controller: 'Group',
    action: 'show',
    locals: {
      layout: 'layoutGroup'
    }
  },

  'GET /group/:gid/load': {
    controller: 'Group',
    action: 'loadGroup'
  },
  
  'GET /group/:gid/loadoneGroupAjax': {
    controller: 'Group',
    action: 'loadoneGroupAjax'
  },  

  'GET /group/:gid/grouppic': {
    controller: 'Group',
    action: 'loadGroupPic'
  },

  'GET /group/show/:id/:eventType': {
    controller: 'Group',
    action: 'show',
    locals: {
      layout: null
    }
  },

  'GET /newgroup': {
    'controller': 'Group',
    'action': 'create'
  },

  'GET /group/:gid/edit': {
    'controller': 'Group',
    'action': 'edit'
  },

  'GET /group/:gid/members': {
    controller: 'Group',
    action: 'showMembers'
  },

  'GET /group/:gid/getmembersinjson':{
    controller: 'Group',
    action: 'getMembersInJson'
  },

  'POST /group/:gid/addgroupuser': {
    'controller': 'Group',
    'action': 'addUserToGroup'
  },

  'POST /group/:gid/removegroupuser': {
    'controller': 'Group',
    'action': 'removeUserFromGroup'
  },

  'POST /group/:gid/addMemberAjax':{
    'controller': 'Group',
    'action': 'addMembersToGroup'
  },

  'POST /group/:gid/importMemberCSV':{
    'controller': 'Group',
    'action': 'importMembersCSVToGroup'
  },

  'POST /group/uploadimage':{
    'controller': 'Group',
    'action': 'uploadImage'
  },

  '/group/user/search': {
    'controller': 'Group',
    'action': 'searchUser'
  },

  '/group/:gid/pastevent': {
    controller: 'Group',
    action: 'showPastEvent'
  },

  '/group/:gid/comingevent': {
    controller: 'Group',
    action: 'showComingEvent'
  },

  '/group/:gid/calendar': {
    controller: 'Group',
    action: 'showCalendar'
  },

  '/group/:gid/calendarinjson': {
    controller: 'Group',
    action: 'showCalendarEvents'
  },

  '/group/imagemanager': {
    controller: 'Group',
    action: 'imageManager'
  },

  'POST /event/s': {
    'controller': 'Event',
    'action': 'upload'
  },

  'POST /updateProfilePicture': {
    'controller': 'User',
    'action': 'updateProfilePicture'
  },

  'GET /group/:gid/photos': {
    controller: 'Photo',
    action: 'galary'
  },

  'GET /photos/:gid/album/:eid': {
    controller: 'Photo',
    action: 'preview'
  },

  'GET /group/:gid/album/:eid/upload': {
    controller: 'Photo',
    action: 'upload'
  },

  'GET /group/:gid/album/:eid/thumbnail': {
    controller: 'Photo',
    action: 'thumbnail'
  },

  'POST /group/:gid/album/:eid/upload': {
    controller: 'Photo',
    action: 'doUpload'
  },


  '/group/:gid/tags': {
    controller: 'Tag',
    action: 'show'
  },

  '/tag/create': {
    controller: 'Tag',
    action: 'create'
  },

  '/tag/new': {
    controller: 'Tag',
    action: 'new'
  },

  '/tag/edit/:id': {
    controller: 'Tag',
    action: 'edit'
  },

  '/tag/update/:id':{
    controller: 'Tag',
    action: 'update'
  },

  '/tag/remove/:id':{
    controller: 'Tag',
    action: 'remove'
  },

  'GET /comment': {
    controller: 'Comment',
    action: 'show'
  },

  'POST /comment': {
    controller: 'Comment',
    action: 'create'
  },  

  'GET /comment/:id/like': {
    controller: 'Comment',
    action: 'getLike'
  },

  'POST /comment/:id/like': {
    controller: 'Comment',
    action: 'updateLike'
  },

  'POST /comment/:id/delete': {
    controller: 'Comment',
    action: 'delete'
  },

  '/comment/:id/replies': {
    controller: 'Comment',
    action: 'showReplies'
  },  
  
  'POST /event/:id/addEventMemberAjax':{
    'controller': 'Event',
    'action': 'addUsersToEvent'
  },

  'POST /event/:id/InviteFriendAjax':{
    'controller': 'Event',
    'action': 'InviteFriendToEvent'
  },

  // test relevant routes config

  '/test': {
    controller: 'Test',
    action: 'index'
  },

  '/group/:gid/questionnaire_entry': {
    controller: 'Questionnaire',
    action: 'index'
  },

  'GET /group/:gid/questionnaire': {
    controller: 'Questionnaire',
    action: 'show'
  },

  'POST /group/:gid/questionnaire': {
    controller: 'Questionnaire',
    action: 'create'
  },

  '/group/:gid/papermanage': {
    controller: 'Test',
    action: 'toManagePaper'
  },

  '/group/:gid/uploadpaper': {
    controller:'Test',
    action:'uploadPaper'
  },

  '/group/:gid/tonewtest': {
    controller: 'Test',
    action: 'toNewTest'
  },

  '/test/ajaxgettest':{
    controller: 'Test',
    action: 'ajaxGetTest'
  },

  '/test/:gid/newtest':{
    controller: 'Test',
    action: 'doNewTest'
  },

  '/group/:gid/tostarttest':{
    controller: 'Test',
    action: 'toStartTest'
  },

  '/group/:gid/starttest':{
    controller: 'Test',
    action: 'startTest'
  },

  '/group/:gid/testmanager':{
    controller: 'Test',
    action: 'toManageTest'
  },

  '/group/:gid/gettestreport':{
    controller:'Test',
    action: 'showReport'
  },

  '/test/:testid/showsimplereport':{
    controller:'Test',
    action: 'showSimpleReport'
  },

  '/test/:testid/showdetailreport':{
    controller: 'Test',
    action: 'showDetailReport'
  },

  '/test/:testid/getdetailreport':{
    controller: 'Test',
    action: 'getDetailReport'
  },

  '/test/submitanswer': {
    controller: 'Test',
    action: 'submitAnswer'
  },

  '/test/destroytest':{
    controller: 'Test',
    action: 'destroyTest'
  },

  '/test/destroypaper':{
    controller: 'Test',
    action: 'destroyPaper'
  },

  '/group/:gid/survey/surveymanage': {
    controller: 'Survey',
    action: 'toManageSurvey'
  },

  '/group/:gid/survey/uploadsurvey': {
    controller:'Survey',
    action:'uploadSurvey'
  },


  '/group/:gid/survey/tostartsurvey':{
    controller: 'Survey',
    action: 'toStartSurvey'
  },

  '/survey/:gid/startsurvey':{
    controller: 'Survey',
    action: 'startSurvey'
  },

  '/survey/submitsurvey': {
    controller: 'Survey',
    action: 'submitSurvey'
  },

  '/survey/:gid/togetreport':{
    controller: 'Survey',
    action: 'toGetReport'
  },

  '/survey/:surveyid/getreport':{
    controller:'Survey',
    action: 'getReport'
  },

  '/survey/:surveyid/getdetailreportdata':{
    controller: 'Survey',
    action: 'getDetailReportData'
  },

  '/group/:gid/survey/destroysurvey':{
    controller: 'Survey',
    action: 'destroySurvey'
  },

  '/group/:gid/filemanage': {
    controller: 'File',
    action: 'toManageFile'
  },

  '/group/:gid/uploadfile': {
    controller:'File',
    action:'uploadFile'
  },



  '/file/destroyfile':{
    controller: 'File',
    action: 'destroyFile'
  },

  '/group/:gid/todownloadfile':{
    controller: 'File',
    action: 'toDownloadFile'
  },

  '/group/:gid/downloadfile':{
    controller: 'File',
    action: 'downloadFile'
  },

  '/group/:gid/getdownloads':{
    controller: 'File',
    action: 'getdownloads'
  },

  '/aboutus' : {
    controller: 'About',
    action: 'showabout'
  },

  '/thanks' : {
    controller: 'About',
    action: 'showcontribution'
  },

  '/admin/showAdminDashboard':{
    controller: 'Admin',
    action: 'showAdminDashboard'
  },

  '/admin/showAdminGlobalPrivilege':{
    controller: 'Admin',
    action: 'showAdminGlobalPrivilege'
  },

  '/admin/showAdminGroupPrivilege':{
    controller: 'Admin',
    action: 'showAdminGroupPrivilege'
  },

  '/admin/showAdminSingleGroupPrivilege':{
    controller: 'Admin',
    action: 'showAdminSingleGroupPrivilege'
  },

  '/admin/showAdminEventPrivilege':{
    controller: 'Admin',
    action: 'showAdminEventPrivilege'
  },

  '/admin/showAdminSingleEventPrivilege':{
    controller: 'Admin',
    action: 'showAdminSingleEventPrivilege'
  },

  '/admin/showAdminRoleManage':{
    controller: 'Admin',
    action: 'showAdminRoleManage'
  },

  '/admin/addOrUpdateAdminRole':{
    controller: 'Admin',
    action: 'addOrUpdateAdminRole'
  },

  '/admin/deleteAdminRole':{
    controller: 'Admin',
    action: 'deleteAdminRole'
  },

  '/admin/getAdminRoleDetail':{
    controller: 'Admin',
    action: 'getAdminRoleDetail'
  },

  '/admin/updateGlobalPrivilege':{
    controller: 'Admin',
    action: 'updateGlobalPrivilege'
  },

  '/admin/updateGroupPrivilege':{
    controller: 'Admin',
    action: 'updateGroupPrivilege'
  },

  '/admin/updateEventPrivilege':{
    controller: 'Admin',
    action: 'updateEventPrivilege'
  },

  '/bigevent':{
    controller: 'Group',
    action: 'showBigEvent'
  },

  '/openday':{
    controller: 'Group',
    action: 'showOpenDay'
  }
  
};
