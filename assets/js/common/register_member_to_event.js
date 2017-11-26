'use strict';

define(['jquery','bootstrap'], function($){
  $(document).ready(function(){
    $('#register_member_btn').click(function(event){
      var btn = $(this);
      hideAlertMsg();
      btn.button('loading');
      var selectedUsersIDList = [];
      var selectedUsers = $('#myPillbox').pillbox('items');
      for(var i=0; i<selectedUsers.length; i++){
        selectedUsersIDList.push(selectedUsers[i].value);
      }
      $.post('/event/'+$('#eid').val()+'/addEventMemberAjax', {
        'users': selectedUsersIDList,
        'eid': $('#eid').val()})
        .done(function(data){
          if(data.error)
          {
            showAlertMsg(data.error);
          }else{

            $('#register_event_member').modal('toggle');
            $('#register_event_member').data('modal',null);
            //$(window).trigger('hashchange');
            window.location.reload();
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
      if(!$('#register_event_member_alert').hasClass('hidden'))
      {
        $('#register_event_member_alert').toggleClass('hidden');
      }
    };

    var showAlertMsg = function(message)
    {
      if(!message)
      {
        message = 'Server or Network error.';
      }
      var dt = '<dt>'.concat(message, '</dt>');
      $('#register_event_member_alert > dl').html(dt);
      $('#register_event_member_alert').removeClass('hidden');
    };

    $('#userselect').keyup(function(event){

      $.ajax({
          url: '/group/user/search',
          data: {
              search: $('#userselect').val(),
              per_page: 20,
              active: !0,
              groupid: $('#gid').val(),
              current_user: 1
          },
          dataType: 'json'
      }).done(function(data) {
          if(data.error)
          {
            alert(data.error);
          }else{
            $('.user-select').css('display','none');
            $('.user-select ul').empty();
            $('.user-select').css('display','block');
            for(var i=0; i<data.user.length; i++){
              $('.user-select ul').append('<li id='+data.user[i].id+' >'+data.user[i].fullname+'</li>');  
            }
          }
      });

    });

    $('.user-for-select').on('click', function(event) {
      var $target = $(event.target);
      if ($target.is('li')) {
        $('#myPillbox').pillbox('addItems', 1, [{ text: $target.html(), value: $target.attr('id'), attr: {}, data: {} }]);
      }
    });


  });
});
