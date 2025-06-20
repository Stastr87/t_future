"""code check"""

from utils.quote_scales.quote_scales import QuotesScales


def show_futures_calculating(figi_list: tuple[str, ...]):
    """Show futures calculating table"""
    scale_obj = QuotesScales(figi_list)
    scale_obj.show_table()
