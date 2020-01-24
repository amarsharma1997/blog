from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField


User = get_user_model()



def upload_location(instance,filename):
    return "%s/%s" %(instance.username,filename)




class postManager(models.Manager):
    def active(self,*args,**kwargs):
        return super(postManager,self).filter(draft=False).filter(publish__lte=timezone.now())

#just overload any function or create any function and just write the definition and put the
#the object in the model class and done just use it



class topic(models.Model):
    topicname = models.CharField(max_length=50)
    followers = models.IntegerField()
    proposed_by = models.ForeignKey(User,on_delete= None)
    description = models.TextField(max_length=200)

    class Meta:
        ordering = ["topicname"]

    def __str__(self):
        return self.topicname


class post(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextUploadingField(blank=True,null=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,null=True,blank=True)
    user = models.ForeignKey(User , default=1,on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)
    draft = models.BooleanField(default=False)
    publish = models.DateTimeField(auto_now=False,auto_now_add=False)
    topic = models.ManyToManyField(topic)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    objects = postManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("posts:detail",kwargs={"slug":self.slug})

    class Meta:
        ordering=["-timestamp","-updated"]


def pre_save_post_receiver(sender,instance,*args,**kwargs):
    slug=slugify(instance.title)
    instances=post.objects.filter(title=instance.title)
    ln=len(instances)+1
    instance.slug = "%s-%s" %(slug,ln)




pre_save.connect(pre_save_post_receiver,post)




class review(models.Model):
    post = models.ForeignKey(post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    type = models.BooleanField()
    timestamp = models.DateTimeField(auto_now=True,auto_now_add=False)

    class Meta:
        ordering = ["-timestamp"]


class comment(models.Model):
    post = models.ForeignKey(post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    commentText = models.TextField(max_length=2000)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

class commentReply(models.Model):
    parentcomment = models.ForeignKey(comment,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    commentText = models.TextField(max_length=2000)
    timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

