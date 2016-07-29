var gulp = require('gulp');
var sass = require('gulp-sass');

gulp.task('styles', function() {
    gulp.src('static/scss/**/*.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('../web/gainful/static/css/'))
});

gulp.task('js', function() {
    gulp.src('static/js/**/*.js')
        .pipe(gulp.dest('../web/gainful/static/js/'))
});

//Watch task
gulp.task('default',function() {
    gulp.watch('static/scss/**/*.scss',['styles']);
    gulp.watch('static/js/**/*.js',['js']);
});
