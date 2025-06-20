"""main app"""

import click

from bin.calculate_futures import show_futures_calculating
from bin.generate_figi_list import generate_base_with_futures


@click.command()
@click.argument("instrument_str", nargs=1)
def main(instrument_str: str = ""):
    """main function call"""
    instruments_figi_list = generate_base_with_futures(instrument_str)
    for item in instruments_figi_list:
        if len(item) > 1:
            show_futures_calculating(tuple(item))


if __name__ == "__main__":
    main()
