const { getGroupUsersMail, findUserFromTheGroup, add_user_to_group, addUsersToGroup, remove_user_from_group } = require('../../lib/groupUtil')
const { assert } = require('chai')
const {init_user, createUser, createGroup} = require('./common')

describe('GroupUtil.getGroupUsersMail', ()=>{
  before(done=>{
    userName = 'yaolin'
    groupName= 'group1'

    Promise.resolve()
    .then(_=> createUser('yaolin', '61467748'))
    .then(_=> createUser('yaolin2', '61467749'))
    .then(_=> User.findOne({uid: userName}))
    .then(user=> createGroup({name: groupName, userIds: ['61467748', '61467749']}, user))
    .then(()=>done())
    .catch(done)
  })

  it('getGroupUsersMail should be correct', (done)=>{

    Promise.resolve()
    .then(_=> Group.findOne({name: groupName}))
    .then(group=> getGroupUsersMail(group.id))
    .then((mails)=>{
      assert.equal(mails.length, 2);
      assert.equal(mails[0], 'yaolin@nokia.com');
      assert.equal(mails[1], 'yaolin2@nokia.com');
    })
    .then(done)
    .catch(done)
  })


  it('getGroupUsersMail groupid not exist', (done)=>{
    const errorGroupid= 12

    Promise.resolve()
    .then(_=> getGroupUsersMail(errorGroupid))
    .then(done)
    .catch(err=>{
      assert.equal(err.message, `no such group, groupId: ${errorGroupid}`)
    })
    .then(done)
    .catch(done)
  })

  it('findUserFromTheGroup should be correct', (done)=>{
    const correctGroupName= groupName
    const correctUser= '61467748'

    Group.findOne({name: correctGroupName})
    .then(group=>findUserFromTheGroup(correctUser, group.id))
    .then((user)=>{
      assert.equal(user._id, correctUser);
    })
    .then(done)
    .catch(done)
  })

  it('findUserFromTheGroup no such user', (done)=>{
    const correctGroupName= groupName
    const errUser= '61467750'

    Group.findOne({name: correctGroupName})
    .then(group=>findUserFromTheGroup(errUser, group.id))
    .catch(err=>{
      assert.equal(err.message, `Could not find user in the group groupid:1, userid: ${errUser}`)
    })
    .then(done)
    .catch(done)
  })

  it('add_user_to_group user already exist', (done)=>{
    const correctGroupName= groupName
    const correctUser= '61467748'

    User.findOne({_id: correctUser})
    .then(user=> add_user_to_group(user._id, 1))
    .then((userId)=>{
      assert.equal(userId, correctUser);
      return Group.findOne({name: correctGroupName})
    })
    .then(group=>{
      assert.equal(group.userIds.length, 2);
      assert.equal(group.userIds[0], 61467748);
      assert.equal(group.userIds[1], 61467749);
    })
    .then(done)
    .catch(done)
  })

  it('add_user_to_group user not exist', (done)=>{
    const correctGroupName= groupName
    const newUser= '61467750'

    createUser('yaolin3', newUser)
    .then(user=> add_user_to_group(user._id, 1))
    .then((userId)=>{
      assert.equal(userId, newUser);
      return Group.findOne({name: correctGroupName})
    })
    .then(group=>{
      assert.equal(group.userIds.length, 3);
      assert.equal(group.userIds[0], 61467748);
      assert.equal(group.userIds[1], 61467749);
      assert.equal(group.userIds[2], 61467750);
    })
    .then(done)
    .catch(done)
  })

  it('remove_user_from_group should be correct', (done)=>{
    const correctGroupName= groupName
    const correctUser= '61467748'

    User.findOne({_id: correctUser })
    .then(user=> remove_user_from_group(user._id, 1))
    .then((userId)=>{
      assert.equal(userId, correctUser);
      return Group.findOne({name: correctGroupName})
    })
    .then(group=>{
      assert.equal(group.userIds.length, 2);
      assert.equal(group.userIds[0], 61467749);
      assert.equal(group.userIds[1], 61467750);
    })
    .then(done)
    .catch(done)
  })

  it('remove_user_from_group user not exest', (done)=>{
    const correctGroupName= groupName
    const invalidUser= '61467751'

    remove_user_from_group(invalidUser, 1)
    .catch((err)=>{
      assert.equal(err.message, `user not in the group, groupId: 1, userId: ${invalidUser}`)
    })
    .then(()=>Group.findOne({name: correctGroupName}))
    .then(group=>{
      assert.equal(group.userIds.length, 2);
      assert.equal(group.userIds[0], 61467749);
      assert.equal(group.userIds[1], 61467750);
    })
    .then(done)
    .catch(done)
  })

  it('addUsersToGroup should be ok', (done)=>{
    const correctGroupName= groupName
    const newUsers = [100, 101, 102, userName ]

    addUsersToGroup(newUsers, 1 )
    .then((userId)=>{
      //assert.equal(userId, newUser);
      return Group.findOne({name: correctGroupName})
    })
    .then(group=>{
      assert.equal(group.userIds.length, 6);
      assert.equal(group.userIds[0], 61467749); //doing wrong
      assert.equal(group.userIds[1], 61467750); //doing wrong
      assert.equal(group.userIds[2], 100);
      assert.equal(group.userIds[3], 101);
      assert.equal(group.userIds[4], 102);
      assert.equal(group.userIds[5], userName);
    })
    .then(done)
    .catch(done)
  })

})

