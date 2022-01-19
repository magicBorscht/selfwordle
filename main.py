import os
import json
import re
import random


LETTERS = 5
TRIES = 6
RUNS = 1
IDEA_OF_A_WORD = ''
VERDICTS = []
AUTOMATIC = True


def import_dicks() -> dict:
    blya = os.listdir('dicts')
    ebalo = {}
    for filename in blya:
        with open(f"dicts/{filename}", "r") as fuck:
            ebalo.update(json.loads(fuck.read()))
    return ebalo


def make_verdict(the_word):
    verdict = ''
    the_hint = ['_' for i in range(LETTERS)]
    avoid = []
    for i, letter in enumerate(the_word):
        if IDEA_OF_A_WORD[i] == letter:
            verdict += 'G'
            the_hint[i] = letter
        elif letter in IDEA_OF_A_WORD:
            verdict += 'Y'
            the_hint.append(f' [{letter}]')
        else:
            verdict += 'F'
            avoid.append(letter)

    print(f"And the verdict iiiiiis..................\n\n{verdict}\n\n{'=' * 20}\n")
    print('the hint:')
    print(''.join(the_hint))
    print(f'Avoid letters {", ".join(avoid)}')
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


def choose_shit_manually(ebalo, tried_words):
    while True:
        the_word = input(f"Input your word. Uppercase, {LETTERS} symbols, no dirty tricks: ")
        if the_word == 'fug':
            return the_word
        if the_word not in ebalo:
            print("This is not in the dictionary, try again.")
        elif the_word in tried_words:
            print("You already tried that, didn't do you well, did it?")
        else:
            return the_word


def run_shit(ebalo, resp):
    i = 0
    the_word = ''
    tried_words = []
    for i in range(TRIES):
        print(f"Attempt number {i + 1}")
        if AUTOMATIC:
            if not resp:
                the_word = random.choice(ebalo)
            else:
                the_word = choose_shit(ebalo, resp, the_word, tried_words)
        else:
            the_word = choose_shit_manually(ebalo, tried_words)
            if the_word == 'fug':
                return False, 0, 'emergency'

        tried_words.append(the_word)

        print(f'THE CHOSEN WORD: {the_word}')
        resp = make_verdict(the_word)
        VERDICTS.append(resp)
        if resp == 'G' * LETTERS:
            return True, i + 1, the_word
    return False, i + 1, 'fuck'


def wordler():
    if not AUTOMATIC:
        print("If you wanna chicken out, just type 'fug' in the prompt. "
              "Be warned, you'll be properly disrespected for that.")
    wins = 0
    loses = 0
    winrate = 0.0
    tries_amounts = []
    global IDEA_OF_A_WORD
    ebalo = [e for e in list(import_dicks().keys()) if len(e) == LETTERS and re.match(r'[A-Z]', e)]
    for i in range(RUNS):
        VERDICTS = []
        resp = ''

        IDEA_OF_A_WORD = random.choice(ebalo)

        victory, tries, the_word = run_shit(ebalo, resp)

        if victory:
            print(f"You still didn't win anything, but your code guessed the word in {tries} tries. It was {the_word}")
            wins += 1
            tries_amounts.append(tries)
        else:
            if the_word == 'emergency':
                print("What a coward.")
                print(f"The word was {IDEA_OF_A_WORD}, by the way")
                return
            else:
                print(f"You lost after {tries} tries. What a shame. You should've tried {IDEA_OF_A_WORD}, maybe.")
            loses += 1

        for verdict in VERDICTS:
            print(verdict)
        print("=" * 8)

    if loses == 0:
        winrate = 'infinite'
    else:
        winrate = round(wins / loses, 2)
    if len(tries_amounts) == 0:
        avg_tries = 'Nobody cares because you lost'
    else:
        avg_tries = sum(tries_amounts) / len(tries_amounts)
    print(f"You won our gorgeous shiny nothing {wins} times and you miserably lost {loses} times.\n"
          f"Your winrate is {winrate}. Average tries: {avg_tries}.")
    return


if __name__ == '__main__':
    wordler()
