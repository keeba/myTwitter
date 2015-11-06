from django.conf.urls import patterns, include, url
from django.contrib import admin
from myTwitter import views
from tweet import views as tweet_views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tweets', tweet_views.TweetViewSet)
router.register(r'users', tweet_views.UserViewSet)
router.register(r'followees', tweet_views.FolloweeViewSet)

urlpatterns = patterns('',
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.home,name='home'),
    url(r'^register/$',views.register,name='register'),
    url(r'^login/$',views.login_user,name='login'),
    url(r'^logout/$',views.logout_user,name='logout'),
    url(r'^api/', include(router.urls)),    
)
