var tweetControllers = angular.module('tweetApp.controllers', []);

tweetControllers.controller('TweetCtrl',['$scope','Tweet','AuthUser','$interval',
	  function TweetCtrl($scope,Tweet,AuthUser,$interval) {
	  $scope.tweets = [];	
	  $scope.authuser = AuthUser;
	  function gettweets(){
		  Tweet.query(function(response) {
		  	$scope.tweets = response;
		  });
	  }
	  gettweets();
	  var tweetsPromise = $interval(gettweets,1000);
	  $scope.$on('$destroy', function () { $interval.cancel(tweetsPromise); });
	  
	  $scope.saveTweet = function(text) {
		  var tweet = new Tweet({text: text});
		  tweet.$save(function(){
			$scope.tweets.unshift(tweet);
		  })
	  }
}]);

tweetControllers.controller('UsersCtrl',['$scope','$state','AuthUser','User','Followee',
	  function UsersCtrl($scope,$state,AuthUser,User,Followee) {
	  $scope.authuser = AuthUser;
	  $scope.users = [];	
	  User.query(function(response) {
		  $scope.users = response;
	  });
	  $scope.saveFollowee = function(followee) {
		  var followee = new Followee({followee:followee,follower:AuthUser.id });
		  followee.$save(function(){
			  $state.go($state.current, {}, {reload: true});
		  });
	  }
	  
	  $scope.deleteFollowee = function(id) {
		  if(Followee.delete({ id:id }))
		  {
			  $state.go($state.current, {}, {reload: true});
		  }
	  }
}]);
