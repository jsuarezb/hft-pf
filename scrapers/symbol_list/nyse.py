import csv

import requests

class Scraper:
    """
    NYSE symbols scraper
    """

    SYMBOLS_PER_PAGE = 10

    SYMBOLS_URI = ('https://www.nyse.com/search?site=idc_instruments'
                   '&client=nyse_frontend_html&proxystylesheet=ice_frontend_json'
                   '&requiredfields=INSTRUMENT_TYPE:EQUITY.NORMALIZED_TICKER:{letter}*'
                   '&getfields=*&num={symbols_per_page}&filter=0&sort=meta:NORMALIZED_TICKER:A'
                   '&start={start}&wc=1000')

    LETTERS = [chr(i) for i in range(ord('A'), ord('Z') + 1)]

    SYMBOL_TICKER = 'SYMBOL_TICKER'
    INSTRUMENT_NAME = 'INSTRUMENT_NAME'


    def scrape(self):
        symbols = [self.__scrap_letter(letter) for letter in Scraper.LETTERS]
        return [[k, v] for letter_dicts in symbols for k, v in letter_dicts.items()]


    def generate_url(self, **kwargs):
        return None


    def write(self, data, path):
        with open(path, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)


    def __scrap_letter(self, letter):
        print('For letter {0}'.format(letter))
        symbols = {}
        current_index = 0

        while True:
            uri = self.SYMBOLS_URI.format(letter=letter, symbols_per_page=self.SYMBOLS_PER_PAGE,
                                          start=current_index)
            response = requests.get(uri)
            json = response.json()
            symbols.update(self.__parse_symbols(json))

            result_navs = json.get('results_nav')
            has_next = self.to_int(result_navs.get('have_next'), 0)
            current_index = self.to_int(result_navs.get('results_end'), 0) + 1

            if has_next != True: # if 2 == True: is True, if 2: is not true
                break

        return symbols


    def __parse_symbols(self, json):
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
