import os
import json
import re
import random
from settings import LETTERS, TRIES, RUNS, AUTOMATIC


class Wordler:
    idea_of_a_word = ''
    verdicts = []
    correct_letters = {}
    shit_letters = set()
    included_letters = set()
    tried_words = []
    ebalo = {}
    verdict = ''
    the_word = ''
    wins = 0
    loses = 0
    winrate = 0.0
    tries_amounts = []
    avg_tries = 0
    victory = False
    tries = 0

    def import_dicks(self):
        blya = os.listdir('dicts')
        temp_shitter = {}
        for filename in blya:
            with open(f"dicts/{filename}", "r") as fuck:
                temp_shitter.update(json.loads(fuck.read()))
        self.ebalo = [e for e in list(temp_shitter.keys()) if len(e) == LETTERS and re.match(r'[A-Z]', e)]

    def make_verdict(self):
        verdict = ''
        for i, letter in enumerate(self.the_word):
            if self.idea_of_a_word[i] == letter:
                verdict += 'G'
                self.correct_letters.update({i: letter})
            elif letter in self.idea_of_a_word:
                verdict += 'Y'
                self.included_letters.update(letter)
            else:
                verdict += 'F'
                self.shit_letters.update(letter)

        print(f"And the verdict iiiiiis..................\n\n{verdict}\n")
        if verdict != "G" * LETTERS:
            print("the hint:")
            print("".join([self.correct_letters.get(i, '_') for i in range(LETTERS)]))
            print(f"Also might be in this word: {', '.join(self.included_letters)}")
            print(f"Avoid letters {', '.join(self.shit_letters)}\n{'=' * 20}\n")
        self.verdict = verdict
        self.verdicts.append(verdict)

    def choose_shit(self):
        for word in set(self.ebalo):
            # print(f"Let's try {word}, shall we")
            yellow_checked = True
            green_checked = True
            grey_checked = True
            if word in self.tried_words:
                # print(f"The word {word} has already been tried with no luck")
                continue
            for letter in self.included_letters:
                if letter not in word:
                    # print(f"The letter {letter} must be in this word, but it isn't")
                    yellow_checked = False
            for letter in self.shit_letters:
                if letter in word:
                    # print(f"The letter {letter} must be not be here")
                    grey_checked = False
            for indox, letter in self.correct_letters.items():
                if word[indox] != letter:
                    # print(f"The letter {letter} must be in {indox + 1} place, but it isn't there")
                    green_checked = False
            if yellow_checked and green_checked and grey_checked:
                self.the_word = word
                return

    def choose_shit_manually(self):
        while True:
            the_word = input(f"Input your word. Uppercase, {LETTERS} symbols, no dirty tricks: ")
            if the_word == 'fug':
                self.the_word = 'emergency'
                return
            if the_word not in self.ebalo:
                print("This is not in the dictionary, try again.")
            elif the_word in self.tried_words:
                print("You already tried that, didn't do you well, did it?")
            else:
                self.the_word = the_word
                break

    def play(self):
        i = 0
        for i in range(TRIES):
            print(f"Attempt number {i + 1}")
            if AUTOMATIC:
                if not self.verdict:
                    self.the_word = random.choice(self.ebalo)
                else:
                    self.choose_shit()
            else:
                self.choose_shit_manually()
                if self.the_word == 'emergency':
                    self.victory = False
                    return

            self.tried_words.append(self.the_word)

            print(f'THE CHOSEN WORD: {self.the_word}')
            self.make_verdict()
            if self.verdict == 'G' * LETTERS:
                self.victory = True
                self.tries = i + 1
                return
        self.victory = False
        self.tries = i + 1
        return

    def run_this_shit(self):
        for i in range(RUNS):
            self.verdicts = []
            self.tries = 0
            self.correct_letters = {}
            self.shit_letters = set()
            self.included_letters = set()
            self.tried_words = []
            self.verdict = ''

            self.idea_of_a_word = random.choice(self.ebalo)

            self.play()

            if self.victory:
                if AUTOMATIC:
                    player = 'this code'
                else:
                    player = 'you'
                print(
                    f"You still didn't win anything, but {player} guessed the word in {self.tries} tries. "
                    f"It was {self.the_word}")
                self.wins += 1
                self.tries_amounts.append(self.tries)
            else:
                if self.the_word == 'emergency':
                    print("What a coward.")
                    print(f"The word was {self.idea_of_a_word}, by the way")
                    return
                else:
                    print(f"You lost after {self.tries} tries. What a shame. "
                          f"You should've tried {self.idea_of_a_word}, maybe.")
                self.loses += 1

            for verdict in self.verdicts:
                print(verdict)
            print("=" * 8)

        if self.loses == 0:
            self.winrate = 'infinite'
        else:
            self.winrate = round(self.wins / self.loses, 2)
        if len(self.tries_amounts) == 0:
            self.avg_tries = 'Nobody cares because you lost'
        else:
            self.avg_tries = sum(self.tries_amounts) / len(self.tries_amounts)
        print(f"You won our gorgeous shiny nothing {self.wins} times and you miserably lost {self.loses} times.\n"
              f"Your winrate is {self.winrate}. Average tries: {self.avg_tries}.")
        return

    def __init__(self):
        self.import_dicks()
        if not AUTOMATIC:
            print("If you wanna chicken out, just type 'fug' in the prompt. "
                  "Be warned, you'll be properly disrespected for that.")

        self.run_this_shit()
