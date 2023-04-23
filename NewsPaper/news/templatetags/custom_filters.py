from django import template

register = template.Library()


@register.filter()
def censor_filter(text: str) -> str:
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
