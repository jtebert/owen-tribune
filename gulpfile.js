// Assuming you already have NodeJS, npm and gulp installed
// and followed instructions at:
// https://www.browsersync.io/docs/gulp/
//
// save this file at <<DJANGO PROJECT ROOT>>
// on your terminal:
// $ cd <<DJANGO PROJECT ROOT>>
// $ gulp

// this will open a browser window with your project
// and reload it whenever a file with the extensions scss,css,html,py,js
// is changed

var gulp = require('gulp');
var browserSync = require('browser-sync');
var reload = browserSync.reload;
var cache = require('gulp-cache');

gulp.task('default', function () {
    browserSync.init({
        notify: false,
        proxy: "localhost:8000"
    });
    gulp.watch(['./**/*.{scss,css,html,py,js}'], ['clear', reload]);
});

gulp.task('clear', function (done) {
    return cache.clearAll(done);
});
