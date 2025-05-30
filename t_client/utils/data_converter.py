"""t client utils"""

from tinkoff.invest import Quotation


def t_quotation_to_float(quotation: Quotation) -> float:
    """Конвертирует данные типа Quotation
    в тип float
    """

    units = float(quotation.units)
    if quotation.nano > 0:
        nano = quotation.nano * 10**-9
    else:
        nano = 0
    value = units + nano
    return value


def tink_money_value_to_float(raw_data) -> float:
    """Конвертирует данные типа MoneyValue в тип float"""
    money_value = raw_data
    units = float(money_value.units)
    if money_value.nano != 0:
        nano = money_value.nano * 10**-9
    else:
        nano = 0
    value = units + nano
    return value
