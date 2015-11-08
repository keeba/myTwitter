from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from tweet.models import Tweet,Followee
from tweet.serializers import TweetSerializer,UserSerializer,FolloweeSerializer
from django.utils import timezone

class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def get_queryset(self):
        """
        Returns lhe last 90 days tweets of the user and user subscribers if the user is logged in,
        else returns the last 90 days tweets of all users.
        """
        reload = 1
        request = self.request
        if request.GET.get('reload'):
            reload = int(self.request.GET['reload'])
        key = 'user-tweets-'
        query_params = {}        
        if request.user.is_authenticated():
            user = request.user
            key += str(user.id)
            key1 = 'user-followees-'+str(user.id)
            followees = user.get_followee_user_ids()
            max_id = request.session.get(key1)
            max_id1 = followees['max_id'] 
            if not max_id or (max_id and max_id != max_id1):
                request.session[key1]=max_id1
                reload = 1                  
            query_params['user_id__in'] = followees['followee_ids']
        else: 
            key += '-all'   
        last_tweet_time = request.session.get(key)  
        if not reload and last_tweet_time:
            query_params['timestamp__gt'] = last_tweet_time
        else:    
            timenow = timezone.now()
            last_90_days = timenow - timezone.timedelta(days=90)
            request.session[key]=timenow            
            query_params['timestamp__gte'] = last_90_days
            query_params['timestamp__lte'] = timenow
        tweets = Tweet.objects.filter(**query_params)    
        if self.request.GET.get('reload'):             
            return tweets
        return tweets
        
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class FolloweeViewSet(viewsets.ModelViewSet):
    queryset = Followee.objects.all()
    serializer_class = FolloweeSerializer
    def perform_create(self,serializer):
        serializer.save(follower=self.request.user)    


