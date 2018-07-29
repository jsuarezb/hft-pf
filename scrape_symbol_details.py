import argparse
import datetime
import sys

import scrapers.symbol_details
from scrapers.symbol_details import google, alphavantage

AVAILABLE_SCRAPERS = {
    scrapers.symbol_details.GOOGLE_FINANCE: google.Scraper,
    scrapers.symbol_details.ALPHA_VANTAGE: alphavantage.Scraper
}


def main():
    args = parse_args()

    scraper = AVAILABLE_SCRAPERS.get(args['source'], None)()
    if scraper is None:
        sys.exit('Unknown source')

    url = scraper.generate_url(args['symbol'])
    data = scraper.scrape(url)

    path = args['destination'] or generate_default_path(args['symbol'], args['source'])
    scraper.write(data, path)


def generate_default_path(symbol, source):
    date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    return '{symbol}-{source}-{date}.csv'.format(symbol=symbol,
                                                 source=source,
                                                 date=date)


def parse_args():
    ap = argparse.ArgumentParser()

    ap.add_argument(
        '-s',
        '--symbol',
        required=True,
        help='Symbol to download details')

    ap.add_argument(
        '--source',
        required=False,
        default=scrapers.symbol_details.GOOGLE_FINANCE,
        help='Source of data. [google_finance]\nDefault: google_finance')

    ap.add_argument(
        '-d',
        '--destination',
        required=False,
        help='Path where to save the results.\nDefault: <symbol>-<source>-<timestamp>.csv')

    return vars(ap.parse_args())


if __name__ == '__main__':
    main()
