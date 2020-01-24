from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,Http404
from .models import post,review,comment,commentReply
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from users.models import UserDetail, History
from django.contrib.auth import get_user_model
from users.views import modified_notifications
import re
from django.db.models import Q
from users.views import UserObject


User = get_user_model()

def getHistory(user):
    #getting the user object to fetch results
    user = get_object_or_404(UserDetail,username=user.username)

    #fetching the tags which has been opened recently
    recently_searched = user.recently_searched_tags
    recently_searched = recently_searched.split('`')

    if recently_searched[0]=='':
        recently_searched=[]

    #getting the topics that he likes
    last_topics = [ current.topicname for current in user.interest_topics.all() ]

    last_topics = last_topics + recently_searched

    #merging them up
    last_topics = set(last_topics)

    return last_topics

class PostSort:
    tags = set()

    def __init__(self,post):
        self.post = post
        self.post_score = 0

        tags = post.topic.all()

        # calculating the tag score for the post
        for current in tags:
            current_tag_name = current.topicname
            if current_tag_name in self.tags:
                self.post_score += 1

    def __lt__(self, other):
        if self.post_score == other.post_score:
            if self.post.views == other.post.views:
                if self.post.likes == other.post.likes:
                    return self.post.unlikes<other.post.unlikes
                return self.post.likes>other.post.likes
            return self.post.views>other.post.views
        return self.post_score>other.post_score


def sortPost(instances,tags_list):
    if not instances:
        return []
    PostSort.tags = tags_list
    new_instances = [ PostSort(current) for current in instances ]
    new_instances.sort()
    new_instances = [current.post for current in new_instances]
    return new_instances



@login_required
def posts_list(request):
    instances = post.objects.active()
    ordering = getHistory(request.user)
    new_instances = sortPost(instances , ordering)
    user = request.user.username
    notifications = len(modified_notifications(request,True,False))
    context={'instances':new_instances, "user":user,'notifications':notifications,"window":1}
    return render(request,'posts/homepage.html',context)


# it is a good practice to have different folder name because at the end it is going to combine all
# the template folders present in different apps at for differentiating all the templates we should
# have folder name for different apps like posts/homepage.html
@login_required
def posts_connections(request):
    instances = post.objects.active()
    user = request.user.username
    user = UserDetail.objects.get(username=user)
    mypeople=[]
    try :
        mypeople = [ current for current in user.following.all() ]
    except ValueError:
        pass
    instances= instances.filter(user__in=mypeople)
    ordering = getHistory(request.user)
    instances = sortPost(instances, ordering)
    context = {'instances': instances, "user": user.username,"window":2}
    return render(request, 'posts/mypeople.html', context)


class post_sort_class:
    def __init__(self,post):
        self.post = post
        self.score=0
        self.user_interest_score = 0

    def inc_score(self):
        self.score += 1

    def __lt__(self, other):
        if self.score == other.score:
            return self.user_interest_score > other.user_interest_score
        return self.score>other.score



@login_required
def posts_search(request):
    print("here")
    query_string = request.GET.get('query')
    user = request.user.username
    notifications = len(modified_notifications(request, True, False))

    posts = post.objects.active()
    query_string = re.split(r'[^a-zA-Z0-9]',query_string)
    new_instances=[]
    users_to_be_searched=[]

    if query_string == '':
        return posts_list(request)

    if request.GET.get('choice')=='Users':
        for query in query_string:
            [users_to_be_searched.append(current) for current in User.objects.filter(Q(username__icontains=query))]
        print(users_to_be_searched)
        lst=[]
        for current in users_to_be_searched:
            userget = UserDetail.objects.get(username=current.username)
            lst.append(UserObject(userget.profile.url, current.first_name, current.last_name, current.username))
        context = { "instances" : lst , 'notifications': notifications, "window": 1}
        return render(request,'posts/users.html',context)


    for query in query_string:
        [ new_instances.append(current) for current in posts.filter(Q(title__icontains=query))]
        [ users_to_be_searched.append(current) for current in User.objects.filter(Q(username__icontains = query )) ]
    [ new_instances.append(current) for current in posts.filter(user__in=users_to_be_searched) ]


    # now sorting process
    map_of_posts={}
    ordering = getHistory(request.user)
    list_of_post_sort=[]
    PostSort.tags = ordering

    for instance in new_instances:
        if map_of_posts.get(instance.slug)==None:
            map_of_posts[instance.slug] = post_sort_class(instance)
            obj = PostSort(instance)
            list_of_post_sort.append(obj)
        map_of_posts[instance.slug].inc_score()

    for instance in list_of_post_sort:
        map_of_posts[instance.post.slug].user_interest_score=instance.post_score

    list_instance = []
    for slug,obj in map_of_posts.items():
        list_instance.append(obj)

    list_instance.sort()
    new_instances = [current.post for current in list_instance ]


    context = {'instances': new_instances, "user": user, 'notifications': notifications, "window": 1}
    return render(request, 'posts/homepage.html', context)


@login_required
def posts_create(request):
    form = PostForm(request.POST or None , request.FILES or None)
    context = {
        'form':form,
        'window':5,
    }
    if form.is_valid():
        instance=form.save(commit=False) #if commit is false then it is not going
        instance.user=request.user
        # to save instance in the database directly. we can do some updates in that and can save with this
        # following method
        instance.save()
        return redirect(instance.get_absolute_url())#httpresponseredirect accepts only url and redirect returns
        #httpresponseredirect and takes models,view or url as input
    return render(request,'posts/form.html',context)
#post.objects.get(id=id)#or as filter(id=id)[0]# get returns only one object and filter returns queryset




@login_required
def posts_update(request,slug=None):
    instance = get_object_or_404(post, slug=slug)
    if request.user != instance.user:
        raise Http404
    form = PostForm(request.POST or None,request.FILES or None, instance=instance)
    context = {'form': form, }
    if form.is_valid():
        instance=form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())  # it accepts only url and redirect returns
    return render(request,'posts/form.html',context)





@login_required
def posts_detail(request,slug=None):
    ruser = request.user
    instance = get_object_or_404(post,slug=slug)

    #whether the requesting user is the author
    master = False
    if instance.user == ruser :
        master = True

    #Finding out all the reviews that are related to this post
    reviews = review.objects.filter(post=instance)

    #counting likes and dislikes
    likes = dislikes = 0
    for rev in reviews:
        if rev.type == True:
            likes +=1
        else:
            dislikes += 1
    userreview = reviews.filter(user=request.user)
    usreviewed=False
    type = False
    if userreview:
        usreviewed=True
        type = userreview[0].type
    comments = comment.objects.filter(post=instance)

    topic_list = instance.topic.all()
    # updating the last_searched field in table UserDetail
    if instance.user != request.user:
        user_in_user_detail = UserDetail.objects.get(username=ruser.username)
        last_tags = user_in_user_detail.recently_searched_tags.split('`')
        if last_tags[0]=='':
            last_tags=[]
        last_tags = [current.topicname for current in topic_list] + last_tags
        length = len(last_tags)
        if length>100:
            last_tags = last_tags[0:100]
        user_in_user_detail.recently_searched_tags = "`".join(last_tags)
        user_in_user_detail.save()


    ## adding a row in history table
    # if instance.user != request.user:
    #     does_exist = History.objects.filter(user=request.user,post=instance).exists()
    #     if not does_exist:
    #         instance.views += 1
    #         instance.save()
    #     newrow = History(post=instance,user=request.user)
    #     newrow.save()
    # #views = History.objects.filter(post=instance).values_list('user',flat=True).distinct().count()
    #it was not a feasible method because each time we have to count again and again instead we could
    #just store count in the instance itself

    context = {
        "requser": request.user,
        "master": master,
        "instance": instance,
        "likes": likes,
        "dislikes": dislikes,
        "user": usreviewed,
        "type": type,
        "comments": comments,
        "views":instance.views,
        "topics":topic_list,
    }

    return render(request,'posts/showdetail.html',context)



@login_required
def posts_delete(request,slug=None):
    instance = get_object_or_404(post, slug=slug)
    if request.user != instance.user:
        raise Http404
    instance.delete()
    return posts_list(request)




@login_required
def posts_like(request,slug=None):
    user = request.user
    instance = get_object_or_404(post,slug=slug)
    rev = review.objects.filter(post=instance,user=user)
    if rev :
        rev = rev[0]
        if rev.type == False:
            rev.type = True
            rev.save()
            instance.dislikes -= 1
            instance.likes += 1
    else:
        instance.likes += 1
        rev = review(post=instance,user=user,type=True)
        rev.save()
    instance.save()
    return redirect(reverse("posts:detail",kwargs={"slug":slug}))




@login_required
def posts_dislike(request,slug=None):
    user = request.user
    instance = get_object_or_404(post, slug=slug)
    rev = review.objects.filter(post=instance, user=user)
    if rev:
        rev = rev[0]
        if rev.type == True:
            rev.type = False
            rev.save()
            instance.likes -= 1
            instance.dislikes += 1
    else:
        instance.dislikes += 1
        rev = review(post=instance,user=user,type=False)
        rev.save()
    instance.save()
    return redirect(reverse("posts:detail", kwargs={"slug":slug}))



@login_required
def posts_comment(request,slug=None):
    user = request.user
    instance = get_object_or_404(post,slug=slug)
    if request.POST.get('comment')=='':
        return redirect(reverse("posts:detail", kwargs={"slug": slug}))
    postcomment = comment(user=user,post=instance,commentText=request.POST.get('comment'))
    postcomment.save()
    return redirect(reverse("posts:detail", kwargs={"slug":slug}))



@login_required
def posts_comment_show(request,thread):
    commentinstance = get_object_or_404(comment,id=thread)
    commentthread = commentinstance.commentreply_set.all().reverse()
    context = {
        'thread':commentthread,
        'instance':commentinstance,
        'user':request.user
    }
    return render(request,'posts/showcomment.html',context)


@login_required
def posts_comment_reply(request,id):
    commentinstance = get_object_or_404(comment,id=id)
    text = request.POST["comment"]
    newinstance = commentReply(commentText=text,parentcomment=commentinstance,user=request.user)
    newinstance.save()
    return redirect(reverse("posts:showcomment",kwargs={"thread":id}))

@login_required
def posts_comment_delete(request,id):
    instance = get_object_or_404(comment,id=id,user=request.user)
    slug=instance.post.slug
    instance.delete()
    return redirect(reverse('posts:detail',kwargs={'slug':slug}))

@login_required
def posts_comment_reply_delete(request,id):
    instance = get_object_or_404(commentReply,id=id,user= request.user)
    red = instance.parentcomment.id
    instance.delete()
    return redirect(reverse('posts:showcomment',kwargs={"thread":red}))



