class Scraper:

    def scrape(url):
        """
        Scrapes a datasource to obtain information.
        """
        raise NotImplementedError

    def generate_url(symbol, **kwargs):
        """
        Generates the url to scrape given the symbol.
        """
        raise NotImplementedError
