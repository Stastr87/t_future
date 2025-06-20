"""quote scales utils"""

from tinkoff.invest import Future, Quotation

from clients.cbr.utils.cbr_utils import get_current_key_rate
from clients.t_client.utils.data_converter import t_quotation_to_float
from utils.common import get_dif
from utils.quote_scales.schema.schema import CalculatedDataSchema


def get_percent_from_value(a, b) -> float:
    """Returns percent value a from b"""

    result = (a / b) * 100
    return result


def get_percent_from_value_as_str(a, b) -> str:
    """Returns percent value a from b as str"""

    if isinstance(a, float) and isinstance(b, float):
        percent = get_percent_from_value(a, b)
        result_str = f"{round(a, 2)} ({round(percent, 2)}%)"
    else:
        result_str = "-"
    return result_str


def get_future_price(future_object: Future, price: Quotation) -> float:
    """Return converted futures price

    Стоимость фьючерсов предоставляется в пунктах.
    Формула для пересчёта:
    price / min_price_increment * min_price_increment_amount
    """
    min_price_increment = t_quotation_to_float(future_object.min_price_increment)
    min_price_increment_amount = t_quotation_to_float(
        future_object.min_price_increment_amount
    )
    price_float = t_quotation_to_float(price)
    basic_asset_size = t_quotation_to_float(future_object.basic_asset_size)
    converted_price = price_float / min_price_increment * min_price_increment_amount
    # Приведение к цене базового инструмента
    normalized_price = converted_price / basic_asset_size

    return normalized_price


def get_fair_future_price(
    base_instrument_price: float, days_to_expiration: int, dividend_value: float
) -> float:
    """Returns fair price for future"""

    # Дневная процентная ставка ЦБ
    cb_key_rate = get_current_key_rate()
    day_key_rate = cb_key_rate / 365
    fair_future_price = (
        base_instrument_price
        + ((base_instrument_price - dividend_value) * day_key_rate / 100)
        * days_to_expiration
    )

    return fair_future_price


def get_fair_future_price_as_str(
    base_instrument_price, days_to_expiration, dividend_value
) -> str:
    """Returns fair price for future as str according base instrument price"""
    result = base_instrument_price

    # Если переданное значение days_to_expiration - число, то инструмент является фьючерсом
    # В противном случае возвращаем цену инструмента обратно т.к. это базовый инструмент
    if (
        (isinstance(days_to_expiration, int))
        and (isinstance(base_instrument_price, float))
        and (isinstance(dividend_value, float))
    ):
        result = round(
            get_fair_future_price(
                base_instrument_price, days_to_expiration, dividend_value
            ),
            2,
        )

    return str(result)


def add_futures_deviation(
    calc_data_set: list[CalculatedDataSchema],
) -> list[CalculatedDataSchema]:
    """Adds the deviation value between futures to data set"""

    for i, item in enumerate(calc_data_set):
        if i == 0:
            continue
        if i == 1:
            dif = get_dif(float(item.fair_price), float(calc_data_set[0].price))
            item.deviation = round(dif, 2)
            continue
        if i > 1:
            dif = get_dif(
                float(calc_data_set[i - 1].fair_price),
                float(calc_data_set[i].fair_price),
            )
            item.deviation = round(dif, 2)

    return calc_data_set
