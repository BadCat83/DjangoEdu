from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from allauth.account.signals import user_signed_up

from .models import PostCategory
from NewsPaper.settings import DEFAULT_FROM_EMAIL, SITE_URL

@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    username = user.username
    html_content = render_to_string(
        'greetings.html',
        {
            'link': f'{SITE_URL}',
            'username': username,
        }
    )
    msg = EmailMultiAlternatives(
        subject=f"Спасибо, что зарегестрировались {username}",
        from_email=DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)


@receiver(m2m_changed, sender=PostCategory)
def send_email(sender, instance, **kwargs) -> None:
    if kwargs['action'] == 'post_add':
        title = instance.title
        text = instance.text
        pk = instance.pk
        post_type, link = ('новость', 'news') if instance.post_type=='NW' else ('статья', 'article')
        categories = instance.category.all()
        users : list[str] = []
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
