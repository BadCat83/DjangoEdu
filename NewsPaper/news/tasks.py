import os
from datetime import datetime, timedelta

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from NewsPaper.settings import SITE_URL

from .models import Post, Category


@shared_task
def send_email_through_celery(pk) -> None:
    post = Post.objects.get(pk=pk)
    post_type, link = ('новость', 'news') if post.post_type == 'NW' else ('статья', 'article')
    categories = post.category.all()
    users: list[str] = []
    for category in categories:
        users += category.subscribers.all()
    if users:
        html_content = render_to_string(
            'post_created.html',
            {
                'link': f'{SITE_URL}/{link}/{post.pk}',
                'post_type': post_type,
                'title': post.title,
                'text': post.text,
            }
        )
        for user in users:
            msg = EmailMultiAlternatives(
                subject=f"{post.title}",
                body=f"Здравствуй, {user.username}. Новая {post_type} в твоём любимом разделе!",
                from_email=os.getenv('EMAIL'),
                to=[user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()


@shared_task
def send_weekly_news():
    users = []
    last_week = datetime.now() - timedelta(days=7)
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
