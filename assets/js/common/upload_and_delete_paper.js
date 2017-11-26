'use strict';

define(['jquery','bootstrap'], function($){
  $(document).ready(function(){

    $('#upload_paper_form').submit(function(event){
      event.preventDefault();
      var btn = $(this);
      hideAlertMsg();
      var paperDesc = $('#paperDesc').val();
      if(paperDesc===''){
        showAlertMsg('Paper Description shall not be empty');
        return;
      }
      if($('#inputPaper').val()===''){
        showAlertMsg('File is not selected');
      }else{
        var filefullname = $('#inputPaper').val();
        var pos=filefullname.lastIndexOf("\\");
        var filename = filefullname.substring(pos+1);
        var existedFiles = [];
        $('table > tbody > tr').each(function () {
          existedFiles.push($.trim($(this).find("td:eq(0)").text())); //1是抓取第二列的文字
        });
        if($.inArray(filename, existedFiles)>-1){    
          showAlertMsg('File with the same name is already existed, please upload another file or use another file name');
        }else{
          $.ajax({
            url: '/group/'+ $('#groupID').val()+'/uploadpaper',
            type: 'POST',
            cache: false,
            data: new FormData($('#upload_paper_form')[0]),
            processData: false,
            dataType: 'json',
            contentType: false
          })
          .done(function(data) {
            if(data.error){
              showAlertMsg(data.error);
            }else{
              if(data==='/login'){
                location.href = '/login';
              }else{
                var tr = '<tr><input type="hidden" value ="' + data.id + '"/><td>'+filename+'</td><td>'+paperDesc +'</td><td>'+data.username+'</td>';
                tr = tr + '<td><input type="button" class="btn btn-sm btn-default pull-right delete_paper_btn" value="Delete" /></td>';
                tr = tr + '</tr>'  
                $("#paper_table").append(tr);
              }
            }
          })
          .fail(function(res) {});
        }  
      }
    });

    var hideAlertMsg = function()
    {
      if(!$('#upload_paper_alert').hasClass('hidden')){
        $('#upload_paper_alert').toggleClass('hidden');
      }
    };

    var showAlertMsg = function(message)
    {
      if(!message){
        message = 'Server or Network error.';
      }
      var dt = '<dt>'.concat(message, '</dt>');
      $('#upload_paper_alert > dl').html(dt);
      $('#upload_paper_alert').removeClass('hidden');
    };

    $('#paper_list_body').on('click', 'input', function(){

      var me = this;
      var paperID= $(this).parent().parent().children(":first").val();

      if($(this).val()==='Delete'){
       
        $.post('/test/destroypaper', {paperid: paperID}, null, 'json')
        .done(function(data){
          if(data.error){
            showAlertMsg(data.error);
          }else{
            if(data==='/login'){
              showAlertMsg('you need login first');
            }else{
              console.log($(this).parent().parent());
              $(me).parent().parent().remove();
            }
          }
        })
        .fail(function(){
          showAlertMsg('something is wrong');
        })
        .always(function(){
        });
      }
    });
    
  });

});
