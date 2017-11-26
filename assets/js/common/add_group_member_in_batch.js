'use strict';

define(['jquery','bootstrap'], function($){
  $(document).ready(function(){

    $('#insert_member_CSV_btn').click(function(event){
      var btn = $(this);
      hideCSVAlertMsg();

      if($('#memberCSV').val()===''){
        showCSVAlertMsg('File is not selected');
      }else{
          btn.button('loading');
          $.ajax({
            url: '/group/'+$('#groupID').val()+'/importMemberCSV',
            type: 'POST',
            cache: false,
            data: new FormData($('#upload_member_CSV_form')[0]),
            processData: false,
            dataType: 'json',
            contentType: false
          })
          .done(function(data) {
            if(data.error){
              showCSVAlertMsg(data.error);
            }else{
              if(data==='/login'){
                location.href = '/login';
              }else{
                $('#importMemberCSV').modal('toggle');
                $('#importMemberCSV').data('modal',null);
                window.location.reload();
              }
            }
          })
          .fail(function(){
           showCSVAlertMsg();
          })
          .always(function(){
            btn.button('reset');
          });

      }
    });


    $('#add_member_btn').click(function(event){
      var btn = $(this);
      hideAlertMsg();
      btn.button('loading');
      $.post('/group/'+$('#groupID').val()+'/addMemberAjax', {'member_list': $.trim($('#member_list').val())}, null, 'json')
        .done(function(data){
          if(data==='/login'){
            location.href = '/login';
          }else{
            if(data.error)
            {
              showAlertMsg(data.error);
            }else{
              $('#addmember').modal('toggle');
              $('#addmember').data('modal',null);
              //$(window).trigger('hashchange');
              window.location.reload();
            }
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
      if(!$('#add_member_alert').hasClass('hidden'))
      {
        $('#add_member_alert').toggleClass('hidden');
      }
    };

    var showAlertMsg = function(message)
    {
      if(!message)
      {
        message = 'Server or Network error.';
      }
      var dt = '<dt>'.concat(message, '</dt>');
      $('#add_member_alert > dl').html(dt);
      $('#add_member_alert').removeClass('hidden');
    };

    var hideCSVAlertMsg = function()
    {
      if(!$('#add_member_CSV_alert').hasClass('hidden'))
      {
        $('#add_member_CSV_alert').toggleClass('hidden');
      }
    };

    var showCSVAlertMsg = function(message)
    {
      if(!message)
      {
        message = 'Server or Network error.';
      }
      var dt = '<dt>'.concat(message, '</dt>');
      $('#add_member_CSV_alert > dl').html(dt);
      $('#add_member_CSV_alert').removeClass('hidden');
    };


  });
});
