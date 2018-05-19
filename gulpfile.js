'use strict';


// Imports
let gulp = require('gulp');
let sass = require('gulp-sass');
let cleanCSS = require('gulp-clean-css');
var concat = require('gulp-concat');
var sourcemaps = require('gulp-sourcemaps');


// Constants
const PATH_STATIC = './static/';
const PATH_CSS = `${PATH_STATIC}css`;
const PATH_SCSS = `${PATH_STATIC}scss`;
const PATH_JS = `${PATH_STATIC}js`;
const PATH_IMG = `${PATH_STATIC}img`;


// Tasks
gulp.task('default', function () {
  console.log(`Hello, world!`);
});

gulp.task('sass', function () {
  return gulp.src(`${PATH_SCSS}/**/*.scss`)
    .pipe(sass().on('error', sass.logError))
    .pipe(cleanCSS({compatibility: 'ie8'}))
    .pipe(gulp.dest(`${PATH_CSS}`));
});

gulp.task('js', function(){
  return gulp.src([`${PATH_JS}/*.js`, `!${PATH_JS}/app.min.js`])
    .pipe(sourcemaps.init())
    .pipe(concat('app.min.js'))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(`${PATH_JS}`))
});

gulp.task('watch', function () {
  gulp.watch(`${PATH_SCSS}/**/*.scss`, ['sass']);
  gulp.watch([`${PATH_JS}/**/*.js`, `!${PATH_JS}/app.min.js`], ['js']);
});
