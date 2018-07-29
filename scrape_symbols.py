import argparse
import datetime

import scrapers.symbol_list
from scrapers.symbol_list import nyse

AVAILABLE_SCRAPERS = {
    scrapers.symbol_list.NYSE: nyse.Scraper
}


def main():
    args = parse_args()
    scraper = AVAILABLE_SCRAPERS.get(args['source'])()
    data = scraper.scrape()
    path = args.get('destination') or generate_default_path(args['source'])
    scraper.write(data, path)


def generate_default_path(source):
    date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    return '{source}-symbol_list-{date}.csv'.format(source=source, date=date)


def parse_args():
    ap = argparse.ArgumentParser()

    ap.add_argument(
        '--source',
        required=True,
        help='Source of data. [nyse]')

    return vars(ap.parse_args())

if __name__ == '__main__':
    main()
