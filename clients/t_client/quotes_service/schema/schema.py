"""Schemas for quotes requests"""

from clients.base_schema import BaseSchema


class FigiListSchema(BaseSchema):
    """Quotes schema"""

    figi_list: list[str]
