from django import forms
from .models import Post
from .templatetags.utils import censor


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'post_author', 'category']

    def clean(self):
        cleaned_data = super().clean()
        text = censor(cleaned_data.get("text"))
        cleaned_data['text'] = text
        return cleaned_data

