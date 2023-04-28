from django import template

from .utils import censor

register = template.Library()


@register.filter()
def censor_filter(text: str) -> str:
    return censor(text)


@register.filter()
def news_formatting(news_count: int) -> str:
    count = news_count % 10
    if count == 1:
        return 'ь'
    elif count in [2, 3, 4] and news_count not in [12, 13, 14]:
        return 'и'
    else:
        return 'ей'


@register.filter()
def posts_formatting(posts_count: int) -> str:
    count = posts_count % 10
    if count == 1:
        return ''
    elif count in [2, 3, 4] and posts_count not in [12, 13, 14]:
        return 'а'
    else:
        return 'ов'


@register.filter()
def articles_formatting(posts_count: int) -> str:
    count = posts_count % 10
    if count == 1:
        return 'ья'
    elif count in [2, 3, 4] and posts_count not in [12, 13, 14]:
        return 'ьи'
    else:
        return 'ей'
