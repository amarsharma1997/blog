from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from account.forms import UserLoginForm,UserModelForm
from django.shortcuts import redirect
from users.models import UserDetail

def login_view(request):
    if request.user.is_authenticated:
        return redirect("/posts")
    form=UserLoginForm(request.POST or None)
    next=request.GET.get("next")
    context={
        "form":form,
        "title":"Login",
    }
    if form.is_valid():
        username=form.cleaned_data.get("username")
        password=form.cleaned_data.get("password")
        user = authenticate(username=username,password=password)
        login(request,user)
        if next:
            return redirect(next)
        return redirect("/posts")
        #return redirect("https://www.google.com")
    return render(request,"account/loginform.html",context)

def register_view(request):
    if request.user.is_authenticated:
        return redirect("/posts")
    form=UserModelForm(request.POST or None)
    context={
        "form":form,
        "title":"Register",
    }
    next = request.GET.get("next")
    if form.is_valid():
        user = form.save(commit=False)
        password=form.cleaned_data.get("password")
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username,password=password)
        login(request,new_user)
        new_instance = UserDetail(username = new_user.username)
        new_instance.save()
        if next:
            return redirect(next)
        return redirect("/posts")
    return render(request,"account/loginform.html",context)

def logout_view(request):
    logout(request)
    return redirect('/login')

def forgotpassword_view(request):
    return render(request,"",)
