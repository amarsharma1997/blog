from django.db import models
from django.contrib.auth import get_user_model
from posts.models import post,topic
from django.utils import timezone


User=get_user_model()

def upload_location(instance,filename):
    return "profile/%s" %(instance.id)

class UserDetail(models.Model):
    username = models.CharField(max_length=150)
    following = models.ManyToManyField(User)
    lastseen = models.DateTimeField(default=timezone.now())
    profile = models.ImageField(upload_to=upload_location, null=True, blank=True)
    interest_topics = models.ManyToManyField(topic)
    recently_searched_tags = models.TextField(max_length=5000,blank=True)

    def __str__(self):
        return self.username


# I am removing this table because each time I would have to find some tags and would need to calculate
# the tag score for sorting

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(post, on_delete=models.CASCADE)


    def __str__(self):
        s = self.user.username + " opened " +  self.post.title
        return s









