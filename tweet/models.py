from django.contrib.auth.models import User
from django.db import models
import itertools

class Tweet(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
    def __str__(self):
        return self.text    

class Followee(models.Model):
    follower = models.ForeignKey(User,related_name="follower")
    followee = models.ForeignKey(User,related_name="followee")
    def __str__(self):
        return self.follower.get_full_name()
    class Meta:
        ordering = ['-id']        
        
def get_followee_user_ids(self):
    followees = self.follower.all()
    followees_dict = { 'max_id':None}
    if followees:
        followees_dict['max_id'] = followees[0].id
    followees = followees.values_list('followee')
    followee_ids = list(itertools.chain(*followees))
    followee_ids.append(self.id)
    followees_dict['followee_ids']=followee_ids
    return followees_dict
User.add_to_class('get_followee_user_ids',get_followee_user_ids)   