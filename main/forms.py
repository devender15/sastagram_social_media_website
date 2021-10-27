from django import forms
from home.models import Post


class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Post
        fields = ('username', 'caption', 'image')