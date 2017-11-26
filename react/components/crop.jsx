import React, { Component } from 'react';
import '../../node_modules/react-cropper/node_modules/cropperjs/dist/cropper.css';
import Cropper from 'react-cropper';
import {BASE_URL} from 'config';
var $=require('jquery');

/* global FileReader */

export default class Crop extends Component {

  constructor(props) {
    super(props);
    this.state = {
      src: BASE_URL + 'images/group_default.jpg',
      cropResult: null,
    };
    this.cropImage = this.cropImage.bind(this);
    this.onChange = this.onChange.bind(this);
    this.useDefaultImage = this.useDefaultImage.bind(this);
  }

  onChange(e) {
    e.preventDefault();
    let files;
    if (e.dataTransfer) {
      files = e.dataTransfer.files;
    } else if (e.target) {
      files = e.target.files;
    }
    const reader = new FileReader();
    reader.onload = () => {
      this.setState({ src: reader.result });      
    };
    reader.readAsDataURL(files[0]);
    
  }

  cropImage() {
    if (typeof this.cropper.getCroppedCanvas() === 'undefined') {
      return;
    }
    // to save file size: 1. use jpeg format 2. image quality is 50%
    var cropResult = this.cropper.getCroppedCanvas().toDataURL("image/jpeg", 0.5); 
    this.setState({
      cropResult: cropResult,
    });
    
    this.props.informCropData(cropResult);    
  }

  useDefaultImage() {
    this.setState({ src: BASE_URL + 'images/group_default.jpg' });  
    $('#selectedFile').val("");
  }

  render() {
    return (
      <div>
        <div style={{ width: '100%' }}>
          <input type="file" onChange={this.onChange} id = "selectedFile" />
          <input type="button" onClick={this.useDefaultImage} value="Use default img" />
          <br />
          <br />
          <Cropper
            style={{ height: "100%", width: "100%" }}
            aspectRatio={360 / 300} //recommended dimension is 360*300px           
            zoomable={true}
            guides={false}
            src={this.state.src?this.state.src:(BASE_URL + 'images/group_default.jpg')}
            ref={cropper => { this.cropper = cropper; }}
          />
        </div>
        <div>
          {/*
          <div className="box" style={{ width: '50%', float: 'right' }}>
            <h1>Preview</h1>
            <div className="img-preview" style={{ width: '100%', float: 'left', height: 300 }} />
          </div>
          */}
          <div className="box" style={{ width: '50%', float: 'left' }}>
            <input type="button" onClick={this.cropImage} value="Crop Image" />            
            <img style={{ width: '100%' }} src={this.state.cropResult} />
          </div>
        </div>
        <br style={{ clear: 'both' }} />
      </div>
    );
  }
}

//export default Crop;