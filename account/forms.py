from django import forms
from django.contrib.auth import get_user_model,authenticate

User=get_user_model()

class UserLoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)

    def clean(self,*args,**kwargs):
        username=self.cleaned_data.get("username")
        password=self.cleaned_data.get("password")
        if username and password:
            user=authenticate(username=username,password=password)
            if not user:
                raise forms.ValidationError("User does not Exist.")
            if not user.check_password(password):
                raise forms.ValidationError("Wrong Password")
            return super(UserLoginForm,self).clean(*args,**kwargs)


class UserModelForm(forms.ModelForm):
    email=forms.EmailField(label="Email")
    email2 = forms.EmailField(label="Confirm Email")
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    first_name =  forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")

    class Meta:
        model=User
        fields=[
            "username",
            "first_name",
            "last_name",
            "email",
            "email2",
            "password",
            "password2",
        ]

    def clean(self,*args,**kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        email = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get("email2")
        password2 = self.cleaned_data.get("password2")
        user = authenticate(username=username,password=password)
        if email != email2:
            raise forms.ValidationError("Emails should match")
        if password !=password2:
            raise forms.ValidationError("Passwords should match")
        if user:
            raise forms.ValidationError("User already exists")
        queryset = User.objects.filter(email=email)
        if queryset.exists():
            raise forms.ValidationError("This email has already been registered")
        return super(UserModelForm,self).clean(*args,**kwargs)

