from rest_framework import serializers
from django.contrib.auth.models import User
from tweet.models import Tweet,Followee

class TweetSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Tweet
        fields = ('id','text', 'user', 'timestamp')
    
    def get_user(self,obj):    
        return obj.user.get_full_name()
        
class FolloweeSerializer(serializers.ModelSerializer):
    follower = serializers.IntegerField(source="user.id",read_only=True)
    class Meta:
        model = Followee
        fields = ('id','followee','follower')

class UserSerializer(serializers.ModelSerializer):
    is_followee = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id','username','first_name','last_name','last_login','is_followee')
                   
    '''returns the followee object id if the logged in user follows the current user else zero'''              
    def get_is_followee(self,obj):
        request = self.context['request']
        if request.user:
            followee = obj.followee.filter(follower_id=request.user.id)[:1]
            if followee:
                return followee[0].id
        return None        
        