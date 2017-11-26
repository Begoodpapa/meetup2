function auth(agent, user){
  return new Promise((resolve, reject)=>{
    agent
    .post('/auth/loginAjax')
    .send({
      uid: user.uid,
      password: '123'
    })
    .end(function(err) {
      if (err){
        reject(err)
      } else{
        resolve()
      }
    });
  })
}

function init_user(user_name, userid){
  var user = {};
  user.uid = user_name;
  user.fullname = user_name;
  user.email = 'gang-layner.wang@nokia.com';
  user._id = userid;
  return user;
};

function createUser(userName, userId){
  let user = {};
  user.uid = userName;
  user.fullname = userName;
  user.email = `${userName}@nokia.com`
  user._id = userId;
  return User.create(user)
}

function createGroup({name, userIds=['61467748', '61467749']}, owner){
  const newGroup = {
    name: name,
    id: 1,
    desc: `${name} desc`,
    owner: owner,
    groupfd: `${name} fd`,
    userIds: userIds,
    tags: `${name} tag`,
    father: null,
  }
  return Group.create(newGroup)
}


function createEvent({name, begindate, enddate}, group){
  const newEvt = {
    topic: name,
    desc: 1,
    address: `${name} address`,
    begindate: begindate,
    enddate: enddate,
    group: group,
  }

  return Event.create(newEvt)
}


function createCommingEvent(group){ 
  return module.exports.createEvent({name: Date.now(), begindate: new Date(0), enddate: new Date('3000-1-1')}, group)
}

function createPassedEvent(group){ 
  return module.exports.createEvent({name: Date.now(), begindate: new Date(0), enddate: new Date('1990-1-1')}, group)
}


module.exports = {auth, init_user, createUser, createGroup, createEvent, createCommingEvent, createPassedEvent}
