"""quote scales utils"""

from tinkoff.invest import Future, Quotation

from t_client.utils.data_converter import t_quotation_to_float


def get_dif(quote_one: float, qoute_two: float):
    """Returns percent diference between two values
    result = ((qoute_two – quote_one) / quote_one) × 100"""

    dif = ((qoute_two - quote_one) / quote_one) * 100
    return dif


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
