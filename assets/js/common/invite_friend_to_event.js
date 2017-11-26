'use strict';

define(['jquery','bootstrap'], function($){
  $(document).ready(function(){
    $('#invite_friend_btn').click(function(event){
      var btn = $(this);
      hideAlertMsg();

      var input = $('#friend_email').val();
      if(!input) {
        showAlertMsg("Pls provide your friend's email.");
        return;
      }

      var email = input;
      if (input.indexOf('@') !== -1) {
        var found = input.match(/\S+@nokia\.com/i);
        if (!found) {
          showAlertMsg("Pls provide a valid Nokia email.");
          return;
        }
      } else {
        email = input + "@nokia.com";
      }

      $.post('/event/'+$('#eventid').val()+'/InviteFriendAjax', {
        'email': email,
        'from': $('#from').val()
      }).done(function(data) {
          if(data.error) {
            showAlertMsg(data.error);
          } else {
            $('#invite_friend_to_event').modal('toggle');
            $('#invite_friend_to_event').data('modal', null);
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
      if(!$('#input_check_alert').hasClass('hidden'))
      {
        $('#input_check_alert').toggleClass('hidden');
      }
    };

    var showAlertMsg = function(message)
    {
      if(!message)
      {
        message = 'Server or Network error.';
      }
      var dt = '<dt>'.concat(message, '</dt>');
      $('#input_check_alert > dl').html(dt);
      $('#input_check_alert').removeClass('hidden');
    };

  });
});
