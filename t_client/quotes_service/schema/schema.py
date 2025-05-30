"""Schemas for quotes requests"""

from t_client.base_schema import BaseSchema


class FigiListSchema(BaseSchema):
    """Quotes schema"""

    figi_list: list[str]
