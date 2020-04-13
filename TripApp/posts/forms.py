from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('name', 'about', 'image', 'tags', 'location')

    def clean_location(self):
        location = self.cleaned_data['location']
        location = location.strip().title()
        return location


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


