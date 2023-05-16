from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Post, PostCategory
from NewsPaper.settings import DEFAULT_FROM_EMAIL


@receiver(m2m_changed, sender=PostCategory)
def send_email(sender, instance, **kwargs) -> None:
    if kwargs['action'] == 'post_add':
        title = instance.title
        text = instance.text
        post_type = 'новость' if instance.post_type=='NW' else 'статья'
        categories = instance.category.all()
        users : list[str] = []
        for category in categories:
            users += category.subscribers.all()
        if users:
            html_content = render_to_string(
                'post_created.html',
                {
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
