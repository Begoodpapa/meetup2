'use strict'; 
import React from 'react';
import {connect} from 'react-redux';
import {Tabs, Tab, Button, Modal} from "react-bootstrap";
import {BASE_URL} from 'config';
var Common = require('../../common.js'); 
var $ = require('jquery');

class DownLoad extends React.Component {

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
	
	//automatic update download counter (counter++)
	handleClick(fileid){					  
	  var aObject = $("#dlfile"+fileid);//the <a> object that clicked
	  var targetObject = aObject.parents("tr").find("td").eq(3);//eq(3) is the td for download counter.
    var currentCount = targetObject.text(); 	  
	  var newCount = parseInt(currentCount) + 1;

		if (newCount&&newCount>0){
			targetObject.text(newCount.toString());
		}
	}

	formFileList(){
		const{
			groupid
		} = this.props;
		
		const fileList = this.state.files;		
		var that = this;
		
		var listArray = fileList.map(function(file){
			var href = BASE_URL + 'group/' + groupid + '/downloadFile?fileid=' + file.id; 
			return(
      	<tr key={file.id} data-id="" data-model="file">
					<td style={{maxWidth:"200px", wordWrap: "break-word"}}>{file.name}</td>
					<td style={{maxWidth:"250px", wordWrap: "break-word"}}>{file.desc}</td>
					<td>{file.owner.fullname}</td>
					<td>{file.downloads}</td>
          <td>
            <a id={"dlfile" + file.id} className="btn btn-default" role="button" href = {href} onClick={that.handleClick.bind(that, file.id)}>Download</a>
          </td>
				</tr> 				
			)
		})	
		return listArray;
	}

  render(){  	
  	 	
  	return(
  		<div>
  		  <div id="respinfo"></div>
				<table className = "table">
				  <thead>
				    <tr>
	            <th>Name</th>
	            <th>Desc</th>
	            <th>Uploader</th>
	            <th>Downloads</th>
	            <th></th>
	            <th></th>
	          </tr>
	        </thead>  
	        <tbody> 
				    {this.formFileList()}		
				  </tbody>
				</table>
			</div>
    )
  }
}

export default connect((state, ownProps) => ({
  auth: state.auth
}) )(DownLoad);
