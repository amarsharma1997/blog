from django.urls import path
from posts.views import posts_comment,posts_connections,posts_list,posts_create,posts_delete,posts_detail,posts_update,posts_like,posts_dislike,posts_comment_show,posts_comment_reply,posts_comment_delete,posts_comment_reply_delete,posts_search
from django.conf.urls import url


app_name='posts'# needed to add this while providing namespace in parent url it creates error

urlpatterns = [
    path('',posts_list,name='list'),#it does not help when it comes to regex
    path('mypeople/',posts_connections,name='mypeople'),
    url(r'^search/', posts_search, name='search'),
    url('^create/',posts_create,name='create'),
    url(r'(?P<slug>[\w-]+)/update/',posts_update,name='update'),#we can either use url or repath because
    url(r'(?P<slug>[\w-]+)/detail/',posts_detail,name='detail'),# it is helpful when we use url
    url(r'delete/(?P<slug>[\w-]+)/',posts_delete,name='delete'),
    url(r'(?P<slug>[\w-]+)/comment/', posts_comment, name='comment'),
    url(r'(?P<slug>[\w-]+)/like/',posts_like,name='like'),
    url(r'(?P<slug>[\w-]+)/dislike/',posts_dislike,name='dislike'),
    url(r'commentreply/(?P<id>\d+)/', posts_comment_reply, name='reply'),
    url(r'(?P<id>\d+)/delete/', posts_comment_delete, name='commentdelete'),
    url(r'(?P<id>\d+)/replydelete/', posts_comment_reply_delete, name='replydelete'),
    url(r'(?P<thread>\d+)/', posts_comment_show, name='showcomment'),
]
