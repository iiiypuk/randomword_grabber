#!/usr/bin/env python3

from time import sleep
import sqlite3
import requests
from bs4 import BeautifulSoup

__author__ = 'Alexander Popov'
__license__ = 'MIT'
__version__ = '1.0.0'
__email__ = 'iiiypuk@fastmail.fm'


def parse():
    r = requests.get('https://randomword.com/')
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    word = soup.find('div', {'id': 'random_word'}).text
    word_definition = soup.find('div', {'id': 'random_word_definition'}).text

    new_word = {'word': word, 'definition':
                word_definition.replace('  ', '')}

    return(new_word)


if __name__ == '__main__':
    # dict for new parsed words
    words = {}

    # open datebase
    db = sqlite3.connect('./words.db')
    cursor = db.cursor()
    
    # create new table if not exist
    try:
        cursor.execute('CREATE TABLE words(word text, definition text)')
    except sqlite3.OperationalError as e:
        print('INFO:', e)

    # start parse words
    try:
        while(True):
            sleep(0.5)

            new_word = parse()
            words[new_word['word']] = new_word['definition']

            print('Parsed', new_word['word'])

    except KeyboardInterrupt:
        for word in words:
            cursor.execute(
                'INSERT INTO words VALUES ("{word}", "{defin}")'
                .format(word=word, defin=words[word]))

        db.commit()
        
        print('Saved %d words.' % len(words))
