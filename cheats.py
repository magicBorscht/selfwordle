"""
Yes, this is basically a cheating mechanism
"""

import os
import json
import re


class Cheats:
    letters: int
    ebalo: list = []
    shit = ''
    included = ''
    right = ''

    def import_dicks(self):
        blya = os.listdir('dicts')
        temp_shitter = {}
        for filename in blya:
            with open(f"dicts/{filename}", "r") as fuck:
                temp_shitter.update(json.loads(fuck.read()))
        self.ebalo = [e for e in list(temp_shitter.keys()) if len(e) == self.letters and re.match(r'[A-Z]', e)]

    def give_me_this_shit(self):
        shit = list(self.shit)
        included = list(self.included)
        right = {}
        for i, letter in enumerate(self.right):
            if letter != '_':
                right[i] = letter
        fucking_words = []

        for word in set(self.ebalo):
            # print(f"Let's try {word}, shall we")

            yellow_checked = True
            green_checked = True
            grey_checked = True
            if word in fucking_words:
                # print(f"The word {word} has already been tried with no luck")
                continue
            for letter in included:
                if letter not in word:
                    # print(f"The letter {letter} must be in this word, but it isn't")
                    yellow_checked = False
            for letter in shit:
                if letter in word:
                    # print(f"The letter {letter} must be not be here")
                    grey_checked = False
            for indox, letter in right.items():
                if word[indox] != letter:
                    # print(f"The letter {letter} must be in {indox + 1} place, but it isn't there")
                    green_checked = False
            if yellow_checked and green_checked and grey_checked:
                fucking_words.append(word)
        print(fucking_words)

    def __init__(self, letters: int, right='', shit='', included=''):
        self.included = included
        self.shit = shit
        self.letters = letters
        self.right = right
        self.import_dicks()
        self.give_me_this_shit()
