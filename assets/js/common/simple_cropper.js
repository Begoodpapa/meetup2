'use strict'
/**
Simple cropper module for crop image at front end.
@imgChooserId: the ID of input field with file type which is used to select image to be cropped.
@origImgId: the ID of img tag which is used to show the original image chosen by imgChooserId.
@previewCanvasId: the ID of canvas which is used to preview the cropped area of selected image.
@cropCB: the callback when user starts to crop the image. The first argument will be the coodinator of cropped image.
*/
define(['jquery','bootstrap', 'jcrop'], function($){
  return function(imgChooserId, origImgId, previewCanvasId, cropCB){
    var jcrop_api; //jcrop api
    var $img = $('#'.concat(origImgId));
    var $chooser = $('#'.concat(imgChooserId));
    var $previewer = $('#'.concat(previewCanvasId));
    var coords = null;

    var drawCropImage = function(cropArea){
      coords = cropArea;
      if(cropCB)
      {
        cropCB(coords);
      }
      if(hasCroppedArea())
      {
        var imgEl = $img.get(0);
        var wRatio = imgEl.naturalWidth/$img.width();
        var hRatio = imgEl.naturalHeight/$img.height();
        var crop_start = Math.round(coords.x*wRatio);
        var crop_end = Math.round(coords.y*hRatio);
        var crop_w = Math.round(coords.w*wRatio);
        var crop_h = Math.round(coords.h*hRatio);
        var canvas = getCanvas();
        canvas.width = crop_w;
        canvas.height = crop_h;
        getCanvasCtx().drawImage(imgEl, crop_start, crop_end, crop_w, crop_h, 0, 0, crop_w, crop_h);
      }else{
        clearCanvas();
      }
    };

    var hasCroppedArea = function()
    {
      return coords && coords.w > 0 && coords.h > 0;
    };

    var getCanvas = function(){
      var canvas = $previewer.get(0);
      return canvas;
    };

    var getCanvasCtx = function(){
      var ctx = getCanvas().getContext('2d');
      return ctx;
    };

    var clearCanvas = function(){
      var ctx = getCanvasCtx();
      var canvas = getCanvas();
      ctx.clearRect(0,0,canvas.width, canvas.height);
    };

    var resetCrop = function(){
      if(jcrop_api){
        jcrop_api.destroy();
      }
      $img.attr('src', '');
      clearCanvas();
    };

    $img.on("load", function(){
        $(this).css({
          'width':'100%',
          height: 'auto'
        });
    }).each(function(){
        // In some case, the image load event can not fire
        // because the image has been loaded earlier or cached.
        // So we need trigger the load event for this situation.
        if(this.complete){
          $(this).trigger('load');
        }
    });

    $chooser.change( function(event) {
       if(typeof event.target.files[0] !== 'undefined')
       {
         resetCrop();
         var tmppath = URL.createObjectURL(event.target.files[0]);
         $img.fadeIn('fast').attr('src',tmppath).Jcrop({
           onChange: drawCropImage,
           onSelect: drawCropImage,
           aspectRatio: 1.1,
         }, function(){
           jcrop_api = this;
           jcrop_api.setSelect([50,100,105,150]);
         });
       }
    });

    return {
      hasCroppedArea: hasCroppedArea,
      getCroppedData: function(){
          if(hasCroppedArea())
          {
            var cvs = getCanvas();
            var data = cvs.toDataURL('image/jpeg');
            //The picture's format is base64 string, which starts with data:/image/jpeg;base64,xxxxxxxxxxx
            //We have to remove the the prefix of "data:/image/jpeg;base64"
            if(data.length<48){
                console.log('Cropped image data error!');
                return null;
            }
            return data.split(',')[1];
          }
          return null;
      }
    };
  };
});
