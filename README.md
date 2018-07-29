# PF HFT

High frequency trading project.

## Setup

This setup works with **Ubuntu 16.04** or greater using **Python 3** and **Pipenv**.

### pip

We'll be using `pip` to manage the project dependencies.

To install it, run:

```bash
sudo apt install python3-pip
```

After installing `pip`, install `pipenv`:

```bash
pip install --user pipenv
```

### Virtual Environment

To install this project dependencies, run:

```bash
pipenv sync
```

## Running the program

There are two executables: `scrape_symbol_details.py` and `scrape_symbols.py`.

Both scripts should be run within the Pipenv environment. Pipenv provides a simple command to do this:

```bash
pipenv run python scrape_symbols.py ...
pipenv run python scrape_symbol_details.py ...
```

### Symbols List

To download a list of symbols available for trading in a specific stock exchange, you should use `scrape_symbols` script.

```
SYNOPSIS
  scrape_symbols.py --source SOURCE [OPTION]

DESCRIPTION
  --source        specifies the data source, available params: [nyse]

  --destination   path of the CSV file to be written with the downloaded data
```


#### Note

As an extra step, to extract the symbols values only, and sort them alphabetically:

```bash
cut -d',' -f1 symbols.csv | sort > sorted_symbols.csv
```

This writes a list of sorted symbols inside a new file called `sorted_symbols.csv`.

### Symbol Details

To download the time series of prices of a specific symbol, `scrape_symbol_details` should be used.

```
SYNOPSIS
  scrape_symbol_details.py -s SYMBOL [OPTION]

DESCRIPTION
  -s, --symbol    symbol name

  --source        specifies the data source, available params: [google_finance, alpha_vantage]

  --destination   path of the CSV file to be written with the downloaded data
```

If you want to consume Alpha Vantage API, `ALPHA_VANTAGE_API_KEY` must be defined. An Alpha Vantage API key can be generated [here](https://www.alphavantage.co/support/#api-key).
