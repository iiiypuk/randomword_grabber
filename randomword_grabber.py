#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import json
from time import sleep


def load_words():
    with open('./words.json', encoding='utf-8') as file:
        words = json.load(file, encoding='utf-8')

        return(words)


def parse():
    r = requests.get('https://randomword.com/')
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    word = soup.find('div', {'id': 'random_word'}).text
    word_definition = soup.find('div', {'id': 'random_word_definition'}).text

    new_word = {'word': word, 'definition':
                [word_definition.replace('  ', '')]}

    return(new_word)


def main(words_data):
    while(True):
        sleep(0.5)
        new_word = parse()

        print(new_word)

        words_data[new_word['word']] = new_word['definition']

        return(words_data)

__author__ = 'Alexander Popov'
__license__ = "MIT"
__version__ = "1.0.1"
__email__ = "iiiypuk@fastmail.fm"

if __name__ == '__main__':
    words = {}

    words = load_words()
    try:
        while(True):
            words = main(words)
    except KeyboardInterrupt:
        with open('./words.json', 'w', encoding='utf-8') as file:
            file.write(
                json.dumps(words, indent=4, ensure_ascii=False))

            print('Saved %d words.' % len(words))

