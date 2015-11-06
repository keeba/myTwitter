from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from tweet.models import Tweet,Followee
from tweet.serializers import TweetSerializer,UserSerializer,FolloweeSerializer
import itertools

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
        if self.request.user.is_authenticated():
            user = self.request.user
            followees = user.follower.all().values_list('followee')
            tweets = Tweet.objects.filter(user_id__in=list(itertools.chain(followees,[user.id])))[:90]
            return tweets      
        else:    
            return Tweet.objects.all()[:90]
        
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class FolloweeViewSet(viewsets.ModelViewSet):
    queryset = Followee.objects.all()
    serializer_class = FolloweeSerializer
    def perform_create(self,serializer):
        serializer.save(follower=self.request.user)    


