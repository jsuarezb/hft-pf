# PF HFT

High frequency trading project.

## Setup

This setup works with **Ubuntu 16.04** or greater using **Python 3**.

### Virtualenv

It's advised to use `virtualenv` to create a virtual environment and install pip dependencies.

To install `virtualenv` run:

```bash
sudo apt install virtualenv
```

Go to the root of the project and create the virtual environment:

```bash
cd hft-pf/
virtualenv env
```

This should create a new folder called `env` inside the project. Inside this folder we will install all the dependencies using `pip`.

To use the virtual environment, **before using `pip`**, activate it with:

```bash
source env/bin/activate
```

### pip

We'll be using `pip` to manage the project dependencies.

To install it, run:

```bash
sudo apt install python3-pip
```

After installing `pip`, make sure that your virtual environment is activated and install all the project dependencies:

```bash
pip install -f requirements.txt
```

## Running the program

As it is right now, there are two main behaviors.

1. Downloading Google Finance data.
2. Downloading NYSE symbols list.

Before running the program, you should comment the code depending on the behavior needed. Inside `hft-pf/main.py` there should be the `main()` method where there's the logic that controls that behavior.

After commenting the appropiate `main()` line, run it with:

```bash
python main.py
```

The NYSE symbols are written in a file called `symbols.csv`, with two columns: the symbol itself (e.g. AAPL) and the long name (e.g. Apple Inc.).

To extract the symbols values only, and sort them alphabetically:

```bash
cut -d',' -f1 symbols.csv | sort > sorted_symbols.csv
```

This writes a list of sorted symbols inside a new file called `sorted_symbols.csv`.
