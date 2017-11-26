define(['jquery','bootstrap'], function($){

  $('#upload_file_form').submit(function(event){
    event.preventDefault();
    var btn = $(this);
    hideAlertMsg();
    var fileDesc = $('#fileDesc').val();
    if(fileDesc===''){
      showAlertMsg('File Description shall not be empty');
      return;
    }
    if($('#inputFile').val()===''){
      showAlertMsg('File is not selected');
    }else{
      var filefullname = $('#inputFile').val();
      var pos=filefullname.lastIndexOf("\\");
      var filename = filefullname.substring(pos+1);
      var existedFiles = [];
      $('table > tbody > tr').each(function () {
        existedFiles.push($.trim($(this).find("td:eq(0)").text())); //1是抓取第二列的文字
      });
      if($.inArray(filename, existedFiles)>-1){    
        showAlertMsg('File with the same name is already existed, please upload another file or use another file name');
      }else{
        $('#myLoader').show();
        $.ajax({
          url: '/group/'+ $('#groupID').val()+'/uploadfile',
          type: 'POST',
          cache: false,
          data: new FormData($('#upload_file_form')[0]),
          processData: false,
          dataType: 'json',
          contentType: false
        })
        .done(function(data) {
          $('#myLoader').hide();
          if(data.error){
            showAlertMsg(data.error);
          }else{
            if(data==='/login'){
              location.href = '/login';
            }else{
              var tr = '<tr><input type="hidden" value ="' + data.id + '"/><td>'+filename+'</td><td>'+fileDesc +'</td><td>'+data.username+'</td>';
              tr = tr + '<td><input type="button" class="btn btn-sm btn-default pull-right delete_file_btn" value="Delete" /></td></tr>';
              $("#file_table").append(tr);
              alert('file uploaded successfully');
            }
          }
        })
        .fail(function(res) {
          $('#myLoader').hide();
          showAlertMsg('Something wrong in file uploading');
        });
      }  
    }
  });

  var hideAlertMsg = function()
  {
    if(!$('#upload_file_alert').hasClass('hidden')){
      $('#upload_file_alert').toggleClass('hidden');
    }
  };

  var showAlertMsg = function(message)
  {
    if(!message){
      message = 'Server or Network error.';
    }
    var dt = '<dt>'.concat(message, '</dt>');
    $('#upload_file_alert > dl').html(dt);
    $('#upload_file_alert').removeClass('hidden');
  };

  $('#file_list_body').on('click', 'input', function(){

    var me = this;
    var fileID= $(this).parent().parent().children(":first").val();

    if($(this).val()==='Delete'){
     
      $.post('/file/destroyfile', {fileid: fileID}, null, 'json')
      .done(function(data){
        if(data.error){
          showAlertMsg(data.error);
        }else{
          if(data==='/login'){
            showAlertMsg('you need login first');
          }else{
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
