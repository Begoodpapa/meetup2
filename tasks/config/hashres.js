/**
 * Hash css and js to forse client browser fresh it.
 *
 * ---------------------------------------------------------------
 *
 * For usage docs see:
 *     https://github.com/gruntjs/grunt-contrib-cssmi://github.com/Luismahou/grunt-hashres
 */
module.exports = function(grunt) {

	grunt.config.set('hashres', {
        // Global options
        options: {
          // Optional. Encoding used to read/write files. Default value 'utf8'
          encoding: 'utf8',
          // Optional. Format used to name the files specified in 'files' property.
          // Default value: '${hash}.${name}.cache.${ext}'
          fileNameFormat: '${name}.${ext}?${hash}',
          // Optional. Should files be renamed or only alter the references to the files
          // Use it with '${name}.${ext}?${hash} to get perfect caching without renaming your files
          // Default value: true
          renameFiles: true
        },
        // hashres is a multitask. Here 'prod' is the name of the subtask. You can have as many as you want.
        prod: {
          // Specific options, override the global ones
          options: {
            // You can override encoding, fileNameFormat or renameFiles
              renameFiles: false
          },
          // Files to hash
          src: [
            // WARNING: These files will be renamed!
            '.tmp/public/js/config.js',
            '.tmp/public/styles/beehive.css'
          ],
          // File that refers to above files and needs to be updated with the hashed name
          dest: ['views/layout.ejs',
                 'views/layoutGroup.ejs',
                 'views/layout_login.ejs',
                 'views/layoutPromote.ejs']
        }

	});

	grunt.loadNpmTasks('grunt-hashres');
};
