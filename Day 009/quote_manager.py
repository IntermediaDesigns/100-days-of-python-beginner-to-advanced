import random


def get_random_quote(quotes):
    return random.choice(quotes)


def add_quote(quotes, quote, author):
    quotes.append((quote, author))


def remove_quote(quotes, index):
    return quotes.pop(index)
