import scrapers.base

class Scraper(scrapers.base.Scraper):

    def generate_url(symbol, **kwargs):
        """
        Generates the url to scrape given the symbol.
        """
        raise NotImplementedError
