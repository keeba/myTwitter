// Resources have the following methods by default:
// get(), query(), save(), remove(), delete()

angular.module('tweetApp.services', ['ngResource'])
  .factory('Tweet', function($resource) {
	  return $resource('/api/tweets/:id/',{ reload: '@reload' });
  })
  .factory('User', function($resource) {
	  return $resource('/api/users/:id/'); 
  })
  .factory('Followee', function($resource) {
	  return $resource('/api/followees/:id/'); 	  
  });

 

