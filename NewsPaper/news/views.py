from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


class PostsList(ListView):
    model = Post
    queryset = Post.objects.filter(post_type='AR').order_by('creation_time')

    template_name = 'posts.html'
    context_object_name = 'posts'


class PostView(DetailView):
    model = Post
    queryset = Post.objects.filter(post_type='AR').order_by('creation_time')
    template_name = 'post.html'
    context_object_name = 'post'


class NewsList(ListView):
    queryset = Post.objects.filter(post_type='NW').order_by('creation_time')

    template_name = 'news.html'
    context_object_name = 'news'


class NewsView(DetailView):
    model = Post
    queryset = Post.objects.filter(post_type='NW').order_by('creation_time')
    template_name = 'detail_news.html'
    context_object_name = 'news'
