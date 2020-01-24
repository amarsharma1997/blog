from .models import post
from django import forms

class PostForm(forms.ModelForm):
    class Meta:
        model=post
        fields =[
            'title',
            'topic',
            'content',
            'image',
            'draft',
            'publish',
        ]

