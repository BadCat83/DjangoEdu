from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from NewsPaper.settings import DEFAULT_FROM_EMAIL, SITE_URL


@shared_task
def send_email_through_celery(instance) -> None:
    title = instance.title
    text = instance.text
    pk = instance.pk
    post_type, link = ('новость', 'news') if instance.post_type == 'NW' else ('статья', 'article')
    categories = instance.category.all()
    users: list[str] = []
    for category in categories:
        users += category.subscribers.all()
    if users:
        html_content = render_to_string(
            'post_created.html',
            {
                'link': f'{SITE_URL}/{link}/{pk}',
                'post_type': post_type,
                'title': title,
                'text': text,
            }
        )
        for user in users:
            msg = EmailMultiAlternatives(
                subject=f"{title}",
                body=f"Здравствуй, {user.username}. Новая {post_type} в твоём любимом разделе!",
                from_email=DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
