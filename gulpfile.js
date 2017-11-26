'use strict';
// npm i --save-dev  gulp gulp-less gulp-util gulp-autoprefixer node-notifier gulp-mocha gulp-notify
var gulp = require('gulp');
var less = require('gulp-less');
var gutil = require('gulp-util');
var browserify = require('gulp-browserify');
var browserify2 = require('browserify');
var rename = require("gulp-rename");

var reactify = require('reactify');
var babel = require('babelify')
var autoprefixer = require('gulp-autoprefixer');
var _notify = require('gulp-notify');
var nn = require('node-notifier');
var react = require('gulp-react');
var mocha = require('gulp-mocha');
var notify = _notify.withReporter(function(options, callback) {
  new nn.Growl().notify(options, callback);
});
var buffer = require('vinyl-buffer');
var source = require('vinyl-source-stream');

var paths = {
  surveyLess: 'assets/styles/survey.less',
  less: 'less/style.less',
  jsx: 'views/jsx/**/*.jsx',
  commentJSX: 'views/jsx/component/comment.jsx',
  survey: 'views/jsx/component/survey.jsx'
};

var dirs = {
  css: 'public/stylesheets/',
  surveyCss: 'assets/styles/',
};

// gulp.task('default', ['less', 'mocha', 'front:js']);
gulp.task('default', ['jsx']);

gulp.task('less', function() {
  return gulp.src(paths.less)
    .pipe(less())
    .on('error', notify.onError({
      message: 'Error: <%= error.message %>',
      emitError: true
    }))
    .on('error', function(e) {
      gutil.log(e);
      this.emit('end');
    })
    .pipe(autoprefixer({
      browsers: ['last 2 versions'],
      cascade: false
    }))
    .pipe(gulp.dest(dirs.css))
    .pipe(notify('Less success!'));
});

gulp.task('survey-less', function() {
  return gulp.src(paths.surveyLess)
    .pipe(less())
    .on('error', notify.onError({
      message: 'Error: <%= error.message %>',
      emitError: true
    }))
    .on('error', function(e) {
      gutil.log(e);
      this.emit('end');
    })
    .pipe(gulp.dest(dirs.surveyCss))
    .pipe(notify('Less success!'));
});


gulp.task('watch', function() {
  gulp.watch(paths.jsx, ['front:js']);
  gulp.watch(['api/**/*.js', 'test/**/*.js'], ['mocha']);
});

gulp.task('front:js', function() {

  return gulp.src('views/jsx/app/*.jsx')
    .pipe(browserify({
      insertGlobals: false,
      debug: false,
      transform: [reactify]
    }))
    .on('error', notify.onError({
      message: 'front:js failed: <%= error.message %>',
      emitError: true
    }))
    .on('error', function(e) {
      gutil.log(e);
      this.emit('end');
    })
    .pipe(rename(function(path) {
      path.extname = '.js';
    }))
    .pipe(gulp.dest('assets/js/react/'))
    .pipe(notify('JSX complete!'));

});


gulp.task('jsx', function() {
  return gulp.src(paths.commentJSX)
    .pipe(react())
    .on('error', notify.onError({
      message: 'Error: <%= error.message %>',
      emitError: true
    }))
    .on('error', function(e) {
      gutil.log(e);
      this.emit('end');
    })
    .pipe(gulp.dest('assets/js/react/'));
});


gulp.task('survey', function() {

  return browserify2(paths.survey)
    .transform('babelify', {presets:['es2015', "react"] })
    .bundle()
    .on('error', notify.onError({
      message: 'Error: <%= error.message %>',
      emitError: true
    }))
    .on('error', function(e) {
      gutil.log(e);
      this.emit('end');
    })
    .pipe(source('Survey.js')) // gives streaming vinyl file object
    .pipe(buffer()) // <----- convert from streaming to buffered vinyl file object
    .pipe(gulp.dest("assets/js/react/"))
});

gulp.task('watchSurvey', function() {
  gulp.watch(paths.survey, ['survey']);
  gulp.watch(paths.surveyLess, ['survey-less']);
});



gulp.task('mocha', function() {
  return gulp.src(['test/**/*.js'], {
      read: false,
    })
    .pipe(mocha({
      reporter: 'nyan',
      timeout: 9000,
      iu: 'bdd'
    }))
    .on('error', notify.onError({
      message: 'mocha failed: <%= error.message %>',
      emitError: false
    }));
});
