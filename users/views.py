from django.shortcuts import render
from django.http import Http404
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404,redirect
from users.models import UserDetail
from posts.models import post,comment,review
from users.forms import ProfileUpdateForm
from django.utils import timezone
from django.contrib.auth import login,authenticate

User = get_user_model()


def myprofile(request):
    username = request.user
    requesting_user = request.user.username
    user = get_object_or_404(User, username=username)
    followers = user.userdetail_set.all()  # all should be in lowercase
    table2user = get_object_or_404(UserDetail, username=username)
    following = table2user.following.all().count()
    isfollow = followers.filter(username=requesting_user).exists()
    followers = followers.count()
    posts = post.objects.active().filter(user=user)
    from posts.views import sortPost, getHistory
    order = getHistory(request.user)
    posts = sortPost(posts, order)
    image = get_object_or_404(UserDetail, username=username).profile
    if image:
        image = image.url
    context = {
        "ruser": requesting_user,
        "user": user,
        "following": following,
        "followers": followers,
        "isfollow": isfollow,
        "posts": posts,
        "image": image,
        "window":3,
    }
    return render(request, 'users/profile.html', context)


def userprofile(request,username):
    requesting_user = request.user.username
    user = get_object_or_404(User,username=username)
    followers = user.userdetail_set.all() #all should be in lowercase
    table2user = get_object_or_404(UserDetail,username=username)
    following = table2user.following.all().count()
    isfollow = followers.filter(username=requesting_user).exists()
    followers = followers.count()
    posts = post.objects.active().filter(user=user)
    from posts.views import sortPost,getHistory
    order = getHistory(request.user)
    posts = sortPost(posts,order)
    image = get_object_or_404(UserDetail,username = username).profile
    if image :
        image=image.url
    context={
        "ruser":requesting_user,
        "user" : user,
        "following":following,
        "followers":followers,
        "isfollow":isfollow,
        "posts":posts,
        "image":image,
    }
    return render(request,'users/profile.html',context)

class UserObject:
    def __init__(self,url,first,last,username):
        self.image = url
        self.name = first + ' ' +last
        self.username = username
    def __str__(self):
        return self.name


def followerslist(request,username):
    user = get_object_or_404(User,username=username)
    followers = user.userdetail_set.all()
    title = username + "'s followers"
    lst=[]
    for current in followers:
        userget = User.objects.get(username = current.username )
        lst.append(UserObject(current.profile.url,userget.first_name,userget.last_name,current.username))
    context={
        "title":title,
        "list":lst,
    }
    return render(request,'users/followlist.html',context)




def followinglist(request,username):
    title = username + " is following"
    user = get_object_or_404(UserDetail,username=username)
    following = user.following.all()
    lst=[]
    for current in following:
        userget = UserDetail.objects.get(username=current.username)
        lst.append(UserObject(userget.profile.url,current.first_name,current.last_name,current.username))
    context = {
        "title": title,
        "list": lst,
    }
    return render(request, 'users/followlist.html', context)



#see this as well
def updateprofile(request,username):
    if request.user.username != username:
        raise Http404
    user=request.user
    red='/user/'+username+'/profile'
    user_in_Userdetail = get_object_or_404(UserDetail,username=user)
    form = ProfileUpdateForm(request.POST or None,request.FILES or None,instance = user_in_Userdetail,initial = { "firstname": user.first_name,
                                                              "lastname": user.last_name,
                                                              "email": user.email,
                                                              },request=request)
    if form.is_valid():
        user.first_name=form.cleaned_data.get('firstname')
        user.last_name = form.cleaned_data.get('lastname')
        user.email = form.cleaned_data.get('email')
        password=form.cleaned_data.get('newpassword')
        user.set_password(password)
        instance = form.save(commit=False)
        instance.save()
        user = authenticate(username=user.username,password = password)
        login(request,user)
        print("done",user)
        return redirect(red)
    return render(request,'users/form.html',{"form":form})




#whenever a person follows someone then a link is created from UserDetail to User
def follow(request,username):
    requesting_user = request.user.username
    red='/user/' + username + '/profile'
    if requesting_user == username:
        return redirect("users:profile")
    print(requesting_user,username)
    user = get_object_or_404(UserDetail,username=requesting_user)
    touser = get_object_or_404(User,username=username)
    user.following.add(touser)
    user.save()
    return redirect(red)




#whenever a person follows someone then the link is removed from UserDetail to User
def unfollow(request,username):
    requesting_user = request.user.username
    red = '/user/' + username + '/profile'
    if requesting_user == username:
        return redirect("users:profile")
    user = get_object_or_404(UserDetail,username=requesting_user)
    touser = get_object_or_404(User, username=username)
    user.following.remove(touser)
    user.save()
    return redirect(red)



def join(part1,part2):
    if part1!='':
        if part2!='':
            return part1+', ' +part2
        else :
            return part1
    else:
        if part2!='':
            return part2
        else:
            return ''



class PostReactions:
    def __init__(self,post,timestamp,likes,comment,dislikes):
        self.likes = likes
        self.comment = comment
        self.dislikes = dislikes
        self.timestamp = timestamp
        self.post = post

    def __str__(self):
        part1=part2=part3=''
        if self.likes > 0:
            part1 = str(self.likes)
            if self.likes>1:
                part1 +=" likes"
            else :
                part1 += " like"
        if self.dislikes > 0:
            part2 = str(self.dislikes)
            if self.dislikes>1:
                part2 +=" dislikes"
            else :
                part2 += " dislike"
        if self.comment > 0:
            part3 = str(self.comment)
            if self.comment>1:
                part3 +=" comments"
            else :
                part3 += " comment"
        notif = part1
        notif = join(notif,part2)
        notif = join(notif,part3)
        return notif

    def __lt__(self, other):
        return (self.timestamp > other.timestamp)






def modified_notifications(request,whichtime,update):
    user = request.user
    userinstance = UserDetail.objects.get(username=user.username)
    lastseen =userinstance.lastseen

    ##Getting all the posts for which we have to show the notifications

    #posts which he has added
    posts_for = []
    posts = post.objects.active(user = user)
    if posts:
        posts = [ current for current in posts ]
        posts_for += (posts)

    #posts on which he has commented
    commented_posts = comment.objects.filter(user = request.user)
    if posts:
        posts = [ current.post for current in commented_posts ]
        posts_for += posts

    posts_dict = {} #For checking whether a post has been checked for the notifications or not

    notifications = [] ##list of all notifications
    #one by one checking for notifications for each post
    for currentpost in posts_for:
        if posts_dict.get(currentpost.slug)==None: #if the post is done or not if not then proceed
            if whichtime:#are we checking for new updates
                likes = currentpost.review_set.filter(type = True,timestamp__gt=lastseen).exclude(user=user)
                dislikes = currentpost.review_set.filter(type = False,timestamp__gt=lastseen).exclude(user=user)
                comments = currentpost.comment_set.filter(timestamp__gt=lastseen).exclude(user=user)
            else:#or we just want to check all the notifications
                likes = currentpost.review_set.filter(type=True).exclude(user=user)
                dislikes = currentpost.review_set.filter(type=False).exclude(user=user)
                comments = currentpost.comment_set.filter().exclude(user=user)
            if not likes and not dislikes and not comments:
                continue
            if likes:
                if comments:
                    if dislikes:
                        timestamp = max(likes[0].timestamp,max(dislikes[0].timestamp,comments[0].timestamp))
                    else:
                        timestamp = max(likes[0].timestamp, comments[0].timestamp)
                else:
                    if dislikes:
                        timestamp = max(likes[0].timestamp, dislikes[0].timestamp)
                    else:
                        timestamp = likes[0].timestamp
            else:
                if comments:
                    if dislikes:
                        timestamp = max(dislikes[0].timestamp,comments[0].timestamp)
                    else:
                        timestamp = comments[0].timestamp
                else:
                    timestamp = dislikes[0].timestamp
            countlikes = likes.count()
            countdislikes = dislikes.count()
            countcomment = comments.count()
            posts_dict[currentpost.slug] = True
            notifications.append(PostReactions(currentpost,timestamp,countlikes,countcomment,countdislikes))
    if update:# whether we are just checking whether there is any new notifications
        userinstance.lastseen = timezone.now()
        userinstance.save()
    notifications.sort()
    return notifications


def my_notifications(request):
    notifications = modified_notifications(request, True, True)
    if not notifications:
        notifications = modified_notifications(request, False, True)
    user = request.user
    return render(request,'users/notifications.html',{"notifications":notifications,"user":user,"window":4})

