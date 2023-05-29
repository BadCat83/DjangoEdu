from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from allauth.account.signals import user_signed_up

from .models import PostCategory
from NewsPaper.settings import DEFAULT_FROM_EMAIL, SITE_URL

from .tasks import send_email_through_celery


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
        send_email_through_celery.delay(instance.pk)
