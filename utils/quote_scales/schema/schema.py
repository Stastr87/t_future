"""Quotes scales schemas"""

from clients.base_schema import BaseSchema


class QuotesScalesResponse(BaseSchema):
    """Quotes scales response schema"""

    instrument_name: str = ""
    figi_id: str = ""
    ticker: str = ""
    currency: str = ""
    price: float = 0


class CalculatedDataSchema(QuotesScalesResponse):
    """Calculated data schema"""

    next_dividends_value: float | str = "-"
    upcoming_dividends_days: int | str = "-"
    dif: float | str = "-"
    days_for_expiration: int | str = "-"
    fair_price: float | str = "-"
    deviation: float | str = "-"
