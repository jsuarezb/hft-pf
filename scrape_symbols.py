import argparse


def main():
    ap = argparse.ArgumentParser()

    ap.add_argument(
        '-s',
        '--symbol',
        required=True,
        help='Activity to run')

    args = vars(ap.parse_args())


if __name__ == '__main__':
    main()
