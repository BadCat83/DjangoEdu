import os
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.http import Http404
from django.template.loader import render_to_string
from NewsPaper.settings import SITE_URL

from ..models import Post, Category


def censor(text: str) -> str:
    if type(text) == str:
        obscene_words = {'редиска', 'свинтус', 'дурак'}
        text = text.split(' ')
        for index, word in enumerate(text):
            word = "".join(symb for symb in word if symb.isalpha())
            if word in obscene_words:
                text[index] = word[0] + '*' * (len(word) - 1)
        return " ".join(text)
    else:
        raise ValueError


def send_every_week_email():
    users = []
    last_week = datetime.now() - timedelta(days=1)
    posts = Post.objects.filter(creation_time__gte=last_week)
    categories = set(posts.values_list('category__category', flat=True))
    for category in categories:
        users += Category.objects.filter(category=category).values_list(
            'subscribers__username',
            'subscribers__email'
        )
    html_content = render_to_string(
        'posts_last_week.html',
        {
            'link': f'{SITE_URL}',
            'posts': posts,
        }
    )
    for user in set(users):
        user_name, user_email = user
        if user_name:
            msg = EmailMultiAlternatives(
                subject=f"Здравствуй, {user_name}.",
                body='',
                from_email=os.getenv('EMAIL'),
                to=[user_email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()


def new_post_nottification(post_type: str, request) -> None:
    title = request.POST['title']
    text = request.POST['text']
    category = request.POST['category']
    users = User.objects.filter(category__id=category)
    if users:
        html_content = render_to_string(
            'post_created.html',
            {
                'post_type': post_type,
                'title': title,
                'text': text,
                # 'link': f'{SITE_URL}/news/{pk}',
            }
        )
        for user in users:
            msg = EmailMultiAlternatives(
                subject=f"{title}",
                body=f"Здравствуй, {user.username}. Новая статья в твоём любимом разделе!",
                from_email=DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()


def check_posts_count(request):
    last_time = datetime.now() - timedelta(days=1)
    last_posts = Post.objects.filter(creation_time__gte=last_time, post_author__username=request.user)
    if last_posts and len(last_posts) >= 3:
        raise Http404("Нельзя публиковать более 3 постов в день!")
