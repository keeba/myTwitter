from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from tweet.models import Tweet,Followee
from tweet.serializers import TweetSerializer,UserSerializer,FolloweeSerializer
import itertools
from django.core.cache import cache
from django.utils import timezone

class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def get_queryset(self):
        """
        Returns lhe latest 90 tweets of the user and user subscribers if the user is logged in,
        else returns the latest 90 tweets.
        """
        reload = int(self.request.GET.get('reload'))
        if self.request.user.is_authenticated():
            user = self.request.user
            key = 'user-tweets-'+str(user.id)            
            followees = user.follower.all().values_list('followee')
            user_ids = list(itertools.chain(*followees))
            user_ids.append(user.id)
            last_tweet_time = cache.get(key)
            if not reload and last_tweet_time:
                tweets = Tweet.objects.filter(user_id__in=user_ids,timestamp__gt=last_tweet_time)
            else:    
                timenow = timezone.now()
                cache.set(key,timenow)
                tweets = Tweet.objects.filter(user_id__in=user_ids,timestamp__lte=timenow)
            return tweets      
        else: 
            key = 'user-tweets-all'   
            last_tweet_time = cache.get(key)
            if not reload and last_tweet_time:
                tweets=Tweet.objects.filter(timestamp__gt=last_tweet_time)
            else:    
                timenow = timezone.now()
                cache.set(key,timenow)
                tweets=Tweet.objects.filter(timestamp__lte=timenow)
        return tweets        
        
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class FolloweeViewSet(viewsets.ModelViewSet):
    queryset = Followee.objects.all()
    serializer_class = FolloweeSerializer
    def perform_create(self,serializer):
        serializer.save(follower=self.request.user)    


