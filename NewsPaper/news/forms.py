from django import forms
from .models import Post
from .templatetags.utils import censor
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as GoogleSignupForm
from django.contrib.auth.models import Group


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'category']

    def clean(self):
        cleaned_data = super().clean()
        text = censor(cleaned_data.get("text"))
        cleaned_data['text'] = text
        return cleaned_data


class BaseRegisterForm(SignupForm):
    def save(self, request):
        user = super(BaseRegisterForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class GoogleRegisterForm(GoogleSignupForm):
    def save(self, request):
        print("in form!")
        user = super(GoogleRegisterForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
