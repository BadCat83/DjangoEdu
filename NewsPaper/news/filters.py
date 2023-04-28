from django import forms
from django.db import models
from django_filters import FilterSet, DateTimeFilter

from .models import Post


class PostFilter(FilterSet):

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'post_author': ['in'],
            'creation_time': ['gt'],
        }
        filter_overrides = {
            models.DateTimeField: {
                'filter_class': DateTimeFilter,
                'extra': lambda f: {
                    'widget': forms.TextInput(attrs={'type': 'date'}),
                },
            },
        }
