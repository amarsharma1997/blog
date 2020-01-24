from django import forms
from django.contrib.auth import get_user_model
from .models import UserDetail

User = get_user_model()

class ProfileUpdateForm(forms.ModelForm):
    firstname = forms.CharField(label='First Name')
    lastname = forms.CharField(label='Last Name')
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Current Password')
    newpassword = forms.CharField(widget=forms.PasswordInput,label='New Password')
    newpassword2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = UserDetail
        fields = [
            "firstname",
            "lastname",
            "email",
            "password",
            "newpassword",
            "newpassword2",
            "profile",
            "interest_topics",
        ]

    # Below will tell how to get request in django and we have add request=request in the form dec
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)

    def clean(self,*args,**kwargs):
        password = self.cleaned_data.get("password")
        newpassword = self.cleaned_data.get("newpassword")
        newpassword2 = self.cleaned_data.get("newpassword2")
        email = self.cleaned_data.get("email")
        user = self.request.user

        if newpassword != newpassword2:
            raise forms.ValidationError("Passwords Should match.")
        query = User.objects.filter(email=email).exists()
        if query and user.email != email :
            raise forms.ValidationError("Email is already in use.")
        if not user.check_password(password):
            raise forms.ValidationError("Password Error.")
        return super(ProfileUpdateForm,self).clean(*args,**kwargs)


