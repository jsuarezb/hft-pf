import collections
import csv
import re
import datetime
import requests
import sys

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

def main(args):
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


if __name__ == '__main__':
    main(sys.argv)
