"""Quotes scales schemas"""

from t_client.base_schema import BaseSchema


class QuotesScalesResponse(BaseSchema):
    """Quotes scales response schema"""

    instrument_name: str = ""
    figi_id: str = ""
    ticker: str = ""
    currency: str = ""
    price: float = 0


class CalculatedDataSchema(QuotesScalesResponse):
    """Calculated data schema"""

    dif: float | str = "-"
    days_for_expiration: int | str = "-"
