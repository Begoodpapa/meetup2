define(['jquery', 'bootstrap'], function($){
  $('#upload_survey_form').submit(function(event){
    event.preventDefault();
    var btn = $(this);
    hideAlertMsg();
    var surveyDesc = $('#surveyDesc').val();
    if(surveyDesc===''){
      showAlertMsg('survey Description shall not be empty');
      return;
    }
    if($('#inputsurvey').val()===''){
      showAlertMsg('File is not selected');
    }else{
      var filefullname = $('#inputsurvey').val();
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
          url: '/group/'+ $('#groupID').val()+'/survey/uploadsurvey',
          type: 'POST',
          cache: false,
          data: new FormData($('#upload_survey_form')[0]),
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
              var tr = '<tr><input type="hidden" value ="' + data.id + '"/><td>'+filename+'</td><td>'+surveyDesc +'</td><td>'+data.username+'</td>';
              tr = tr + '<td><input type="button" class="btn btn-sm btn-default pull-right delete_survey_btn" value="Delete" /></td>';
              tr = tr + '<td><input type="button" class="btn btn-sm btn-default pull-right get_survey_report_btn" value="Report" /></td>'
              tr = tr + '</tr>'  
              $("#survey_table").append(tr);
            }
          }
        })
        .fail(function(res) {});
      }  
    }
  });

  var hideAlertMsg = function()
  {
    if(!$('#upload_survey_alert').hasClass('hidden')){
      $('#upload_survey_alert').toggleClass('hidden');
    }
  };

  var showAlertMsg = function(message)
  {
    if(!message){
      message = 'Server or Network error.';
    }
    var dt = '<dt>'.concat(message, '</dt>');
    $('#upload_survey_alert > dl').html(dt);
    $('#upload_survey_alert').removeClass('hidden');
  };

  $('#survey_list_body').on('click', 'input', function(){

    var me = this;
    var surveyID= $(this).parent().parent().children(":first").val();

    if($(this).val()==='Delete'){
     
      $.post('/group/'+ $('#groupID').val()+'/survey/destroysurvey', {surveyid: surveyID}, null, 'json')
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
    }else if($(this).val()==='Report'){
      location.href = '/survey/report/'+surveyID;
    }

  });  
})
