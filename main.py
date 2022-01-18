import os
import json
import re
import random


LETTERS = 5
TRIES = 6
IDEA_OF_A_WORD = ''


def import_dicks() -> dict:
    blya = os.listdir('dicts')
    ebalo = {}
    for filename in blya:
        with open(f"dicts/{filename}", "r") as fuck:
            ebalo.update(json.loads(fuck.read()))
    return ebalo


def make_verdict(the_word):
    verdict = ''
    for i, letter in enumerate(the_word):
        if IDEA_OF_A_WORD[i] == letter:
            verdict += 'G'
        elif letter in IDEA_OF_A_WORD:
            verdict += 'Y'
        else:
            verdict += 'F'
    return verdict


def choose_shit(ebalo, resp, the_word, tried_words):
    included_letters = []
    correct_letters = {}
    shit_letters = []
    for i, verdict in enumerate(resp):
        if verdict == 'G':
            correct_letters[i] = the_word[i]
        if verdict == 'Y':
            included_letters.append(the_word[i])
        if verdict == 'F':
            shit_letters.append(the_word[i])

    print('Ebugging blyat')
    print(resp)
    print(included_letters)
    print(correct_letters)
    print(shit_letters)
    print('')

    for word in set(ebalo):
        # print(f"Let's try {word}, shall we")
        yellow_checked = True
        green_checked = True
        grey_checked = True
        if word in tried_words:
            # print(f"The word {word} has already been tried with no luck")
            continue
        for letter in included_letters:
            if letter not in word:
                # print(f"The letter {letter} must be in this word, but it isn't")
                yellow_checked = False
        for letter in shit_letters:
            if letter in word:
                # print(f"The letter {letter} must be not be here")
                grey_checked = False
        for indox, letter in correct_letters.items():
            if word[indox] != letter:
                # print(f"The letter {letter} must be in {indox + 1} place, but it isn't there")
                green_checked = False
        if yellow_checked and green_checked and grey_checked:
            return word

    return 'piss'


def run_shit(ebalo, resp):
    i = 0
    the_word = ''
    tried_words = []
    for i in range(TRIES):
        print(f"Attempt number {i + 1}")
        if not resp:
            the_word = random.choice(ebalo)
        else:
            the_word = choose_shit(ebalo, resp, the_word, tried_words)

        tried_words.append(the_word)

        print(f'THE CHOSEN WORD: {the_word}')
        resp = make_verdict(the_word)
        print(f"And the verdict iiiiiis..................")
        print('')
        print(resp)
        print('')
        print("=" * 20)
        print('')
        if resp == 'G' * LETTERS:
            return True, i + 1, the_word
    return False, i + 1, 'fuck'


if __name__ == '__main__':
    resp = ''
    ebalo = [e for e in list(import_dicks().keys()) if len(e) == LETTERS and re.match(r'[A-Z]', e)]
    IDEA_OF_A_WORD = random.choice(ebalo)
    print('THE WORD IS')
    print(IDEA_OF_A_WORD)

    victory, tries, the_word = run_shit(ebalo, resp)

    if victory:
        print(f"You still didn't win anything, but your code guessed the word in {tries} tries. It was {the_word}")
    else:
        print(f"You lost after {tries} tries. What a shame.")
