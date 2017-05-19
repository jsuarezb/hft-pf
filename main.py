import collections
import csv
import datetime
import re
import requests
import sys

from functools import reduce

GOOGLE_URI = 'https://www.google.com/finance/getprices?i=60&p=100d&f=d,o,h,l,c,v&df=cpct&q={symbol}'

Tick = collections.namedtuple('Tick', ['date', 'open', 'close', 'low', 'high', 'volume'])

class GoogleParser:

    DATETIME_FORMAT = '%Y-%m-%d %H:%M'

    def __init__(self, text):
        self.ticks = self.parse_text(text)

    def parse_text(self, text):
        text = text.replace('%3D', '=') # TODO: improve this
        headers = self.parse_headers(text)
        print(headers)
        return self.parse_ticks(text, headers)

    def parse_headers(self, text):
        header_lines = [line for line in text.split('\n') if '=' in line]
        header_pairs = [line.split('=') for line in header_lines]
        return {pair[0]: pair[1] for pair in header_pairs}

    def parse_ticks(self, text, headers):
        lines = text.split('\n')
        last_header_line_index = max(i for i, line in enumerate(lines) if '=' in line)
        first_tick_line_index = last_header_line_index + 1
        ticks_lines = lines[first_tick_line_index:-1]

        ticks = []
        current_date = None
        for line in ticks_lines:
            if line.startswith('a'):
                opening_date = self.parse_opening_date(line, headers)
                tick_date = opening_date
            else:
                tick_date = self.minute_offset(line, opening_date)

            tick = self.parse_tick(line, tick_date)
            ticks.append(tick)

        return ticks

    def minute_offset(self, line, current_date):
        values = line.split(',')
        minute = int(values[0])
        return current_date + datetime.timedelta(minutes=minute)

    def parse_opening_date(self, line, headers):
        match = re.search('a(.*?),', line)
        if match:
            seconds = int(match.group(1))
            current_date = datetime.datetime.fromtimestamp(seconds)
            timezone_offset = int(headers['TIMEZONE_OFFSET'])
            return current_date + datetime.timedelta(minutes=timezone_offset)

    def parse_tick(self, line, current_date):
        values = line.split(',')
        return Tick(date=current_date.strftime(GoogleParser.DATETIME_FORMAT),
                    open=float(values[4]),
                    close=float(values[1]),
                    high=float(values[2]),
                    low=float(values[3]),
                    volume=float(values[5]))

FILENAME_FORMAT = 'google-{}.csv'
HEADER_ROW = ['date', 'open', 'close', 'low', 'high', 'volume']

def scrap_google():
    symbol = input('Enter the symbol: ')
    data = {'symbol': symbol}
    uri = GOOGLE_URI.format(**data)
    page = requests.get(uri)
    parser = GoogleParser(page.text)
    filepath = FILENAME_FORMAT.format(symbol)

    with open(filepath, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(HEADER_ROW)
        writer.writerows(parser.ticks)

    print('Done.')

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
    # scrap_google()
    scrap_symbols()

if __name__ == '__main__':
    main(sys.argv)
