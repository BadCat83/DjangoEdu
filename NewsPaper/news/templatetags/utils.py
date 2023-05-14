from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from NewsPaper.settings import DEFAULT_FROM_EMAIL


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


def send_email(post_type: str, request) -> None:
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
