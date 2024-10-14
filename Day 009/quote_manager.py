import random


def get_random_quote(quotes):
    return random.choice(quotes)


def add_quote(quotes, quote, author):
    quotes.append((quote, author))


def remove_quote(quotes, quote_to_remove, author_to_remove):
    for index, (quote, author) in enumerate(quotes):
        if quote == quote_to_remove and author == author_to_remove:
            return quotes.pop(index)
    print("Quote not found.")
    print()
    return None
