var path = require('path');
module.exports.upload = {
	calender: path.join(__dirname, '..', 'calenders'),
	photo: {
		root: '/imgs/',
		maxSize: 10, //MB
		thumbSize: [160, 120, 'thumb'],  //[width, height, prefix/alias]
		smallSize: [400, 300, 'small'],
		mediumSize: [1024, 768, 'medium'],
		largeSize: [1600, 1200, 'large']
	},
	eventpic: {
		root: '/pic/',
		maxSize: 3 //MB
	},

	//used to upload group head image 
	groupHead:{
		root:'/imgs/group_head/'
	},

	//used to upload user personal portrait
	portrait:{
		root:'/imgs/portrait/'
	}
};
