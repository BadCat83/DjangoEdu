def censor(text):
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