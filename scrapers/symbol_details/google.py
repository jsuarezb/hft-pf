import csv
import datetime
import re

import requests

import scrapers.symbol_details.base
import tick

class Scraper(scrapers.symbol_details.base.Scraper):
    """
    Google Finance scraper.
    """

    DATETIME_FORMAT = '%Y-%m-%d %H:%M'
    HEADER_ROW = ['date', 'open', 'close', 'low', 'high', 'volume']
    GOOGLE_FINANCE_URL = ('https://www.google.com/finance/getprices'
                          '?i=60&p=100d&f=d,o,h,l,c,v&df=cpct&q={symbol}')


    def scrape(self, url):
        print('Scraping ' + url)
        return requests.get(url).text


    def generate_url(self, symbol):
        return Scraper.GOOGLE_FINANCE_URL.format(symbol=symbol)


    def write(self, data, path):
        data = data.replace('%3D', '=')
        headers = self.__parse_headers(data)
        ticks = self.__parse_ticks(data, headers)

        with open(path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(Scraper.HEADER_ROW)
            writer.writerows(ticks)


    def __parse_headers(self, text):
        header_lines = [line for line in text.split('\n') if '=' in line]
        header_pairs = [line.split('=') for line in header_lines]
        return {pair[0]: pair[1] for pair in header_pairs}


    def __parse_ticks(self, text, headers):
        lines = text.split('\n')
        last_header_line_index = max(i for i, line in enumerate(lines) if '=' in line)
        first_tick_line_index = last_header_line_index + 1
        ticks_lines = lines[first_tick_line_index:-1]

        ticks = []
        current_date = None
        for line in ticks_lines:
            if line.startswith('a'):
                opening_date = self.__parse_opening_date(line, headers)
                tick_date = opening_date
            else:
                tick_date = self.__minute_offset(line, opening_date)

            tick = self.__parse_tick(line, tick_date)
            ticks.append(tick)

        return ticks


    def __minute_offset(self, line, current_date):
        values = line.split(',')
        minute = int(values[0])
        return current_date + datetime.timedelta(minutes=minute)


    def __parse_opening_date(self, line, headers):
        match = re.search('a(.*?),', line)
        if match:
            seconds = int(match.group(1))
            current_date = datetime.datetime.fromtimestamp(seconds)
            timezone_offset = int(headers['TIMEZONE_OFFSET'])
            return current_date + datetime.timedelta(minutes=timezone_offset)


    def __parse_tick(self, line, current_date):
        values = line.split(',')
        return tick.Tick(date=current_date.strftime(Scraper.DATETIME_FORMAT),
                         open=float(values[4]),
                         close=float(values[1]),
                         high=float(values[2]),
                         low=float(values[3]),
                         volume=float(values[5]))
