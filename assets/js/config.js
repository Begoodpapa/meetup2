'use strict';

require.config({
  baseUrl: '/vender',
  waitSeconds: 200,

  paths: {
    jquery: 'jquery/dist/jquery.min',
    react: 'react/react.min',
    bootstrap: 'bootstrap/dist/js/bootstrap.min',
    fuelux: 'fuelux/dist/js/fuelux.min',
    pickmeup: '../js/pickmeup/jquery.pickmeup.min',
    comment: '../js/react/comment',
    jcrop: '../js/jcrop/jquery.Jcrop.min', //TODO use brower to manage it?
    hashchange: '../js/hashchange/hashchange.min',
    'jquery-blueimp-gallery': 'blueimp-gallery/js/jquery.blueimp-gallery',
    'blueimp-gallery': 'blueimp-gallery/js/blueimp-gallery',
    'blueimp-helper': 'blueimp-gallery/js/blueimp-helper',
    'blueimp-bootstrap-image-gallery': 'blueimp-bootstrap-image-gallery/js/bootstrap-image-gallery.min',
    dropzone: 'dropzone/dist/min/dropzone-amd-module.min',
    xhEditor: 'xhEditor/dist/xheditor-1.2.1.min',
    waypoints: 'waypoints/lib/jquery.waypoints.min',
    d3: 'd3/d3.min',
    moment: 'moment/min/moment.min',
    fullcalendar: 'fullcalendar/dist/fullcalendar.min',
    kindeditor: 'kindeditor/kindeditor-min',
    'jquery-mousewheel': 'jquery-mousewheel/jquery.mousewheel.min',
    'php-date-formatter': 'php-date-formatter/js/php-date-formatter.min',
    datetimepicker: 'datetimepicker/build/jquery.datetimepicker.min',
    common: '../js/common',
    masonry: 'masonry/dist/masonry.pkgd.min',
    underscore: 'underscore/underscore-min'
  },

  shim: {
    bootstrap: {
      deps: ['jquery'],
      exports: 'bootstrap'
    },
    pickmeup: {
      deps: ['jquery'],
      exports: 'pickmeup'
    },
    jcrop: {
      deps: ['jquery'],
      exports: 'jquery-jcrop'
    },
    hashchange: {
      deps: ['jquery'],
      exports: 'jquery-hashchange'
    },
    xhEditor: {
      deps: ['jquery'],
      exports: 'jquery-xhEditor'
    },
    React: {
      exports: 'React'
    },
    waypoints: {
      deps: ['jquery'],
      exports: 'waypoints'
    },
    kindeditor:{
      exports: 'kindeditor'
    },
    comment: {
      deps: ['react'],
      exports: 'Comment',
      init: function( React ){
        this.React = React;
      }
    }
  }
});

//Loading JQuery and Bootstrap firstly by default.
require(['jquery','bootstrap']);
