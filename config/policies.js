/**
 * Policy Mappings
 * (sails.config.policies)
 *
 * Policies are simple functions which run **before** your controllers.
 * You can apply one or more policies to a given controller, or protect
 * its actions individually.
 *
 * Any policy file (e.g. `api/policies/authenticated.js`) can be accessed
 * below by its filename, minus the extension, (e.g. "authenticated")
 *
 * For more information on how policies work, see:
 * http://sailsjs.org/#/documentation/concepts/Policies
 *
 * For more information on configuring policies, check out:
 * http://sailsjs.org/#/documentation/reference/sails.config/sails.config.policies.html
 */


module.exports.policies = {

  /***************************************************************************
   *                                                                          *
   * Default policy for all controllers and actions (`true` allows public     *
   * access)                                                                  *
   *                                                                          *
   ***************************************************************************/

  '*': ['poweredby'],
  
  AuthController: {
    logout: ['sessionAuth']
  },

  EventController: {
    create: ['sessionAuth'],
    edit: ['sessionAuth'],
    doEdit: ['sessionAuth', 'privilegeCheck'],
    publish : ['sessionAuth', 'privilegeCheck'],
    upload: ['sessionAuth'],
    addUserToEvent: ['sessionAuth'],
    addUsersToEvent: ['sessionAuth', 'privilegeCheck'],
    InviteFriendToEvent: ['sessionAuth', 'privilegeCheck'],
    removeUserFromEvent: ['sessionAuth'],
  },
  
  GroupController: {
    create: ['sessionAuth'],
    newGroup: ['sessionAuth'],
    remove: ['sessionAuth'],
    updateGroup: ['sessionAuth'],
    edit: ['sessionAuth'],
    addUserToGroup: ['sessionAuth'],
    importMembersCSVToGroup: ['sessionAuth', 'privilegeCheck'],
    removeUserFromGroup: ['sessionAuth'],
    addMembersToGroup:['sessionAuth', 'privilegeCheck'],
  },

  UserController: {
    create: ['sessionAuth'],
    show_my_group: ['sessionAuth'],
    show_my_event: ['sessionAuth'],
    updateProfilePicture: ['sessionAuth'],
    show_my_profile: ['sessionAuth']
  },

  PhotoController: {
    upload: ['sessionAuth'],
    doUpload: ['sessionAuth']
  },

  TestController: {
    toManagePaper: ['sessionAuth'],
    startTest: ['sessionAuth'],
    uploadPaper:  ['sessionAuth', 'privilegeCheck'],
    destroyPaper: ['sessionAuth', 'privilegeCheck'],
    showDetailReport: ['sessionAuth', 'privilegeCheck'],
    getDetailReport: ['sessionAuth', 'privilegeCheck'],
    destroyTest: ['sessionAuth','privilegeCheck']
  },

  SurveyController: {
    toManageSurvey: ['sessionAuth'],
    startSurvey: ['sessionAuth'],
  },

  FileController: {
    toManageFile: ['sessionAuth'],
    destroyFile:  ['sessionAuth', 'privilegeCheck'],
  },

  AdminController: {
    showAdminDashboard: ['sessionAuth', 'privilegeCheck'],
    showAdminGlobalPrivilege: ['sessionAuth', 'privilegeCheck'],
    showAdminGroupPrivilege: ['sessionAuth', 'privilegeCheck'],
    showAdminSingleGroupPrivilege: ['sessionAuth', 'privilegeCheck'],
    showAdminEventPrivilege: ['sessionAuth', 'privilegeCheck'],
    showAdminSingleEventPrivilege: ['sessionAuth', 'privilegeCheck'],
    showAdminRoleManage: ['sessionAuth', 'privilegeCheck'],
    addOrUpdateAdminRole: ['sessionAuth', 'privilegeCheck'],
    deleteAdminRole: ['sessionAuth', 'privilegeCheck'],
    updateGlobalPrivilege: ['sessionAuth', 'privilegeCheck'],
    updateGroupPrivilege: ['sessionAuth', 'privilegeCheck'],
    updateEventPrivilege: ['sessionAuth', 'privilegeCheck'],    
  },

  /***************************************************************************
   *                                                                          *
   * Here's an example of mapping some policies to run before a controller    *
   * and its actions                                                          *
   *                                                                          *
   ***************************************************************************/
  // RabbitController: {

  // Apply the `false` policy as the default for all of RabbitController's actions
  // (`false` prevents all access, which ensures that nothing bad happens to our rabbits)
  // '*': false,

  // For the action `nurture`, apply the 'isRabbitMother' policy
  // (this overrides `false` above)
  // nurture	: 'isRabbitMother',

  // Apply the `isNiceToAnimals` AND `hasRabbitFood` policies
  // before letting any users feed our rabbits
  // feed : ['isNiceToAnimals', 'hasRabbitFood']
  // }
};
