import argparse
import collections
import csv
import datetime
import re
import requests
import sys

from functools import reduce

Tick = collections.namedtuple('Tick', ['date', 'open', 'close', 'low', 'high', 'volume'])

class NyseScrapper:

    SYMBOLS_PER_PAGE = 10

    SYMBOLS_URI = ('https://www.nyse.com/search?site=idc_instruments'
                   '&client=nyse_frontend_html&proxystylesheet=ice_frontend_json'
                   '&requiredfields=INSTRUMENT_TYPE:EQUITY.NORMALIZED_TICKER:{letter}*'
                   '&getfields=*&num={symbols_per_page}&filter=0&sort=meta:NORMALIZED_TICKER:A'
                   '&start={start}&wc=1000')

    LETTERS = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

    SYMBOL_TICKER = 'SYMBOL_TICKER'
    INSTRUMENT_NAME = 'INSTRUMENT_NAME'

    def scrap(self):
        symbols = [self.scrap_letter(letter) for letter in NyseScrapper.LETTERS]
        return [[k, v] for letter_dicts in symbols for k, v in letter_dicts.items()]

    def scrap_letter(self, letter):
        print('For letter {0}'.format(letter))
        symbols = {}
        current_index = 0

        while True:
            uri = self.SYMBOLS_URI.format(letter=letter, symbols_per_page=self.SYMBOLS_PER_PAGE,
                                          start=current_index)
            response = requests.get(uri)
            json = response.json()
            symbols.update(self.parse_symbols(json))

            result_navs = json.get('results_nav')
            has_next = self.to_int(result_navs.get('have_next'), 0)
            current_index = self.to_int(result_navs.get('results_end'), 0) + 1

            if has_next != True: # if 2 == True: is True, if 2: is not true
                break

        return symbols

    def parse_symbols(self, json):
        symbols = {}

        for result in json.get('results', []):
            meta_tags = result.get('meta_tags', [])
            symbol_tickers = [tag.get('value') for tag in meta_tags if tag['name'] == self.SYMBOL_TICKER]
            instrument_names = [tag.get('value') for tag in meta_tags if tag['name'] == self.INSTRUMENT_NAME]

            if symbol_tickers: symbol_ticker = symbol_tickers[0]
            if instrument_names: instrument_name = instrument_names[0]

            symbols[symbol_ticker] = instrument_name

        return symbols

    def to_int(self, x, default):
        return default if x is None or not x else int(x)


def scrap_symbols():
    scrapper = NyseScrapper()
    data = scrapper.scrap()

    with open('symbols.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

    print('Done.')


def main(args):
    ap = argparse.ArgumentParser()

    ap.add_argument(
        '-a',
        '--activity',
        required=True,
        help='Activity to run')

    ap.add_argument(
        '-s',
        '--symbol',
        required=False,
        help='Symbol to download data from')

    args = vars(ap.parse_args())

    if args['activity'] == activities.SYMBOLS:
        pass
    elif args['activity'] == activities.SYMBOL_DETAIL:
        pass
    else:
        print('Unknown action')


if __name__ == '__main__':
    main()
