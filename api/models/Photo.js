'user strict'

/**
 * Photo.js
 *
 * @description :: Photo model to represent the properties of one photo upgraded by users
 */

module.exports = {

  attributes: {
    original: 'string',
    origSize: 'integer',
    origName: 'string',
    origType: 'string',
    thumbnail: 'string',
    small: 'string',
    medium: 'string',
    large: 'string',
    owner: {
      model: 'User'
    },
    album: {
      model: 'Event'
    }
  },

  findAllByAlbum: function(albumId, cb)
  {
    Photo.find({album: albumId})
      .populate('album')
      .populate('owner')
      .exec(function(err, photos){
        if(err)
        {
          sails.log.error(err);
          return cb(err);
        }
        if(photos === 'undefined' || photos.length === 0)
        {
          Event.findOne({id: albumId})
            .exec(function(err, event){
              return cb(null, {
                album: event,
                photos: []
              });
            });
        } else {
          return cb(null, {
            album: photos[0].album,
            photos: photos
          });
        }
      });
  }

};
