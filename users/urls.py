from django.conf.urls import url
from users.views import my_notifications,followerslist,followinglist,updateprofile,userprofile,follow,unfollow,myprofile

app_name='users'

urlpatterns=[
    url(r'^myprofile/',myprofile,name='myprofile'),
    url(r'^(?P<username>[\w-]+)/profile/',userprofile,name='profile'),
    url(r'^(?P<username>[\w-]+)/followers/',followerslist,name='followers'),
    url(r'^(?P<username>[\w-]+)/following/',followinglist,name='following'),
    url(r'^(?P<username>[\w-]+)/updateprofile/',updateprofile,name='update'),
    url(r'^(?P<username>[\w-]+)/follow/',follow,name='follow'),
    url(r'^(?P<username>[\w-]+)/unfollow/',unfollow,name='unfollow'),
    url(r'notifications/',my_notifications,name='notifications'),
]

