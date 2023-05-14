from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Post

@receiver(post_save, sender=Post)
def send_email(sender, instance, created, **kwargs) -> None:
    if created:
        print(instance)
        print(sender)
    else:
        pass
    # title = request.POST['title']
    # text = request.POST['text']
    # category = request.POST['category']
    # users = User.objects.filter(category__id=category)
    # if users:
    #     html_content = render_to_string(
    #         'post_created.html',
    #         {
    #             'post_type': post_type,
    #             'title': title,
    #             'text': text,
    #         }
    #     )
    #     for user in users:
    #         msg = EmailMultiAlternatives(
    #             subject=f"{title}",
    #             body=f"Здравствуй, {user.username}. Новая статья в твоём любимом разделе!",
    #             from_email=DEFAULT_FROM_EMAIL,
    #             to=[user.email],
    #         )
    #         msg.attach_alternative(html_content, "text/html")
    #         msg.send()
