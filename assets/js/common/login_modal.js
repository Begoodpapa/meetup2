'use strict';

define(['jquery','bootstrap'], function($){
  $(document).ready(function(){
    $('#login_btn').click(function(event){
      event.preventDefault();
      var btn = $(this);
      hideAlertMsg();
      btn.button('loading');
      $.post('/auth/loginAjax', $('#login_form').serialize())
        .done(function(data){
          if(data.error)
          {
            showAlertMsg(data.error);
          }else{
            var user = data.user;
            var navbarRightHtml = buildNavbarRightHtml(user);

            $('#header-login').remove();
            $('#header-nav').append(navbarRightHtml);
            $('#fixbar-login').remove();
            $('#fixbar-nav').append(navbarRightHtml);
            $('#page-hearder-right').html(navbarRightHtml);
            $('#loginModal').modal('hide');
            if(!(typeof mediator === 'undefined')){
              mediator.send('login', user);
            }
            $('#event-comments-section').trigger('login', user);

          }
        })
        .fail(function(){
          showAlertMsg();
        })
        .always(function(){
          btn.button('reset');
        });
    });

    var hideAlertMsg = function()
    {
      if(!$('#login_alert').hasClass('hidden'))
      {
        $('#login_alert').toggleClass('hidden');
      }
    };

    var showAlertMsg = function(message)
    {
      if(!message)
      {
        message = 'Server or Network error.';
      }
      var dt = '<dt>'.concat(message, '</dt>');
      $('#login_alert > dl').html(dt);
      $('#login_alert').removeClass('hidden');
    };

    var buildNavbarRightHtml = function(user){

      var newHtml = [];
      var newImgUrl;
      newHtml.push('<li>');
      newHtml.push('<a href="/auth/logout">Log out</a>');
      newHtml.push('</li>');
      newHtml.push('<li class="dropdown">');
      newHtml.push('<a data-target="#" href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">');
      newHtml.push('<span id="username">'.concat(user.fullname, '</span>'));
      newHtml.push('<span class="caret"></span>');
      newHtml.push('</a>');
      newHtml.push('<ul class="dropdown-menu" role="menu">');
      newHtml.push('<li><a href="/user/myprofile">My Profile</a>');
      newHtml.push('</li>');
      newHtml.push('<li><a href="/user/mygroup">My Group</a>');
      newHtml.push('</li>');
      newHtml.push('<li><a href="/user/myevent">My Event</a>');
      newHtml.push('</li>');
      newHtml.push('</ul>');
      newHtml.push('</li>');
      newHtml.push('<li>');
      if(!user.userfd){
        newHtml.push('<img src="/images/default_upp.jpg" alt="..." class="img-circle portrait" ,id ="nav_user_fd">');
      }else{
        newImgUrl = '<img src="'+ user.userfd +'"'+'alt="..." class="img-circle portrait" ,id ="nav_user_fd">';
        newHtml.push(newImgUrl);
      }
      newHtml.push('</li>');
      return newHtml.join('\r\n');
    }
  });
});
