'use strict';

define(['jquery','bootstrap'], function($){
  $(document).ready(function(){

    $('#response_box').on('click', function(event){
      var abtn;
      var userfd, useritem;
      var target = $(event.target);
      if (target.hasClass('userleftevent')){

        abtn = target;
        $.post('/event/leftevent/'+$('#eid').val(), {}, null, 'json')
        .done(function(data){
          if(data==='/login'){
            location.href = '/login';
          }else{
            if(data.error)
            {
              alert(data.error);
            }else{
              $('#event-user-list-ul li').remove('li[userid='+data.id+']');
              abtn.text('join');
              abtn.removeClass('userleftevent');
              abtn.addClass('userjoinevent');
            }
          }
          
        })
        .fail(function(){
          alert('user left failed');
        });
      }
      else if(target.hasClass('userjoinevent')){
        abtn = target;
        $.post('/event/joinevent/'+$('#eid').val(), {}, null, 'json')
        .done(function(data){
          if(data==='/login'){
            $('#loginModal').modal('toggle');
          }else{
            if(data.error)
            {
              alert(data.error);
            }else{
              userfd = data.userfd ? data.userfd : '/images/default_upp.jpg';
              useritem ='<li userid='+data.id+'><img src="'+ userfd + '" alt="..." class="img-circle portrait" ,id ="nav_user_fd">';
              useritem = useritem + '<a href="#/user/'+data.id +'/profile">'+ data.fullname +'</a></li>';
              $('#event-user-list-ul').append(useritem);
              abtn.text('leave');
              abtn.removeClass('userjoinevent');
              abtn.addClass('userleftevent');
            }
          }
        })
        .fail(function(){
          alert('user join failed');
        });
      }
      
    });

  });
});
