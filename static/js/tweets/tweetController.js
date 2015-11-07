var tweetControllers = angular.module('tweetApp.controllers', []);

tweetControllers.controller('TweetCtrl',['$scope','Tweet','AuthUser','$interval',
	  function TweetCtrl($scope,Tweet,AuthUser,$interval) {
	  $scope.tweets = [];	
	  $scope.authuser = AuthUser;
	  $scope.reload = 0;	  
	  Tweet.query({reload:1},function(response) {
	  	$scope.tweets = response;
	  });
	  function getnewtweets(){
		  Tweet.query({reload:$scope.reload},function(response) {
			  if($scope.reload){
			  	  $scope.tweets = response;	
			      $scope.newtweets = null;				  	
			  }
			  else
			  {
			      $scope.newtweets = response;
			  }  
			  $scope.reload =0;
			  $scope.show_new_tweets = 0;
		  });
	  }
	  var tweetsPromise = $interval(getnewtweets,10000);
	  $scope.$on('$destroy', function () { $interval.cancel(tweetsPromise); }); 
	  
	  $scope.saveTweet = function(text) {
		  var tweet = new Tweet({text: text});
		  tweet.$save(function(){
			  if($scope.newtweets)
			  {
			  	  $scope.newtweets.unshift(tweet);
				  $scope.show_new_tweets = 1;
			  }
			  else
			  {
			  	  $scope.tweets.unshift(tweet);
			  }
  		      $scope.reload=1;			
		  })
	  }
	  $scope.showNewTweets = function() {
		  $scope.show_new_tweets = 1;		  
		  $scope.reload=1;
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
