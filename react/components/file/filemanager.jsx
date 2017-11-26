'use strict'; 
import React from 'react';
import {connect} from 'react-redux';
import {Tabs, Tab} from "react-bootstrap";
import {BASE_URL} from 'config';
var Common = require('../../common.js'); 
var $ = require('jquery');

class FileMgr extends React.Component {

	constructor(props){
		super(props);
		
		this.state=({
			files:[]
		})
	}
	
	componentDidMount(){
		const{
			groupid
		} = this.props;
		
    var returnobj = Common.getfilelist(groupid);
    
    if ((returnobj.files)&&(returnobj.files.length>0)){
			this.setState({
    		files: returnobj.files
      })    	
    }else if((returnobj.error)&&(returnobj.error.length > 0)){    
      $('#respinfo').html('<h3>Get file list error.</h3>');
    }
	}	
	
	formFileList(){
		const fileList = this.state.files;		
		var that = this;
		
		var listArray = fileList.map(function(file){
			return(
      	<tr key={file.id} data-id="" data-model="file">
					<td style={{maxWidth:"200px", wordWrap: "break-word"}}>{file.name}</td>
					<td style={{maxWidth:"250px", wordWrap: "break-word"}}>{file.desc}</td>
					<td>{file.owner.fullname}</td>
					<td>{file.downloads}</td>
          <td>
            <a className="btn btn-default" role="button" onClick = {that.deleteFile.bind(this, file.id)}>Delete</a>
          </td>
				</tr> 				
			)
		})	
		return listArray;
	}
	
  hideAlertMsg = ()=>
  {
    if(!$('#upload_file_alert').hasClass('hidden')){
      $('#upload_file_alert').toggleClass('hidden');
    }
  };

  showAlertMsg = (message)=>
  {
    if(!message){
      message = 'Server or Network error.';
    }
    var dt = '<dt>'.concat(message, '</dt>');
    $('#upload_file_alert > dl').html(dt);
    $('#upload_file_alert').removeClass('hidden');
  };	
	
	uploadFile = (e)=>{
		const{
			auth,
			groupid
		} = this.props;
		
		if (!auth.authenticated){
      this.showAlertMsg('You need to sign in before uploading');
      return;			
		}
		
    e.preventDefault();
    var btn = $(this);
    this.hideAlertMsg();
    var fileDesc = $('#fileDesc').val();
    if(fileDesc===''){
      this.showAlertMsg('File Description shall not be empty');
      return;
    }
    if($('#inputFile').val()===''){
      this.showAlertMsg('File is not selected');
    }else{
      var filefullname = $('#inputFile').val();     
      var pos=filefullname.lastIndexOf("\\");
      var filename = filefullname.substring(pos+1);
      var existedFiles = [];
      var that = this;
      
      //TODO handle the file with the same name as any of existing files. is it allowed?
      
      //$('#myLoader').show();
      $.ajax({
        url: BASE_URL + 'group/'+ groupid +'/uploadfile',
        type: 'POST',
        cache: false,
        data: new FormData($('#upload_file_form')[0]),
        processData: false,
        dataType: 'json',
        contentType: false
      })
      .done(function(data) {
        //$('#myLoader').hide();
        if(data.error){
          that.showAlertMsg(data.error);
        }else{
          if(data==='/login'){
            //location.href = '/login';
            that.showAlertMsg('You need to sign in before uploading');
          }else{
            var tr = '<tr><input type="hidden" value ="' + data.id + '"/><td>'+filename+'</td><td>'+fileDesc +'</td><td>'+data.username+'</td>'+'<td>0</td>';
            tr = tr + '<td><a class="btn btn-default" role="button">Delete</a></td></tr>';
            $("#file_table").append(tr);
            alert('file uploaded successfully');
          }
        }
      })
      .fail(function(res) {
       // $('#myLoader').hide();
        that.showAlertMsg('Something wrong in file uploading');
      });
    }        	
	}
	
	deleteFile = (fileid)=>{ 
		const{
			groupid
		} = this.props;
		
		var url = BASE_URL + 'file/destroyfile?fileid=' + fileid; 
		
		$.get(url, function(data, result){			
			if (data.error){								
				alert("Delete file failed.Error:" + data.error);					
			}else {	
				alert("Delete file successful");	
				location.reload();
		  }		
    })		
	}
	
  render(){  	
  	 	
  	return(
		<div className="panel panel-default">
	    <div className="panel-body">
	    
        <Tabs defaultActiveKey={1} id="filetab">
					<Tab eventKey={1} title="Existed Files">
						<table className='table' id='file_table'>
		          <thead>
		            <tr>
			            <th>Name</th>
			            <th>Desc</th>
			            <th>Owner</th>
			            <th>Downloads</th>			            
			            <th></th>
		            </tr>
		            </thead>
		            <tbody id='file_list_body'>
				          {this.formFileList()}		                		                
		            </tbody>
		        </table>										
					</Tab>
					<Tab eventKey={2} title="Upload A File">
						<div id="upload_file_alert" className="alert alert-danger hidden" role="alert">
		          <dl>
		          </dl>
		        </div>
		        <form id="upload_file_form" method="POST" role="form" encType="multipart/form-data">
		          <br/ >
		          <div className="form-group">
		            <label htmlFor="fileDesc">File Description</label>
		            <input type="text" className="form-control" id="fileDesc" name="filedesc" placeholder="File Description" />
		          </div>
		
		          <div className="form-group">
		            <label htmlFor="inputFile">File Input</label>
		            <input id="inputFile" type="file" name="groupfile" />
		          </div>
		
		          <button type="submit" className="btn btn-primary" id="upload_file_btn" onClick={this.uploadFile}>Submit</button>
		        </form>						
					</Tab>
			  </Tabs>	           	       
	    </div>
		</div>
    )
  }
}

export default connect((state, ownProps) => ({
  auth: state.auth
}) )(FileMgr);
