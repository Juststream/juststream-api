import random

with open("words.txt") as reader:
    words_list = [word.strip() for word in reader.readlines()]


def get_random_name():
    return (
        random.choice(words_list).capitalize()
        + random.choice(words_list).capitalize()
        + random.choice(words_list).capitalize()
    )
