import os
import requests

import scrapers.symbol_details.base

class Scraper(scrapers.symbol_details.base.Scraper):
    """
    Alpha Vantage scraper
    """
    INTRADAY_URL = ('https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY'
                    '&symbol={symbol}&interval=1min&apikey={api_key}&outputsize=full'
                    '&datatype=csv')

    def scrape(self, url):
        return requests.get(url).text


    def generate_url(self, symbol):
        return Scraper.INTRADAY_URL.format(symbol=symbol, api_key=self.__api_key())


    def write(self, data, path):
        with open(path, 'w') as f:
            f.write(data)


    def __api_key(self):
        return os.environ['ALPHA_VANTAGE_API_KEY']
