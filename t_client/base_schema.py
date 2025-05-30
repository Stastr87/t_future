"""Common channel schema"""

from typing import Optional

from pydantic import BaseModel


class ResponseCommonSchema(BaseModel):
    """Common error channel schema"""

    success: bool
    message: Optional[str] = None


class BaseSchema(BaseModel):
    """Common channel schema class"""

    @classmethod
    def get_field_names(cls, alias=False):
        """Get class attributes"""
        return list(cls.model_json_schema(alias).get("properties").keys())
