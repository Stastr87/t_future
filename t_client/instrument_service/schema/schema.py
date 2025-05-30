"""Schemas for instruments service"""
from datetime import datetime

from pydantic import RootModel
from t_client.base_schema import BaseSchema


class NormalizedDividendsSchema(BaseSchema):
    """Normalized dividends schema"""
    last_buy_date: datetime
    value: float
    currency: str



class DividendsSchema(BaseSchema, RootModel):
    """Dividends schema"""
    root: list[NormalizedDividendsSchema]
