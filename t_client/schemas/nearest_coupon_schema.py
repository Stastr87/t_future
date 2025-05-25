"""Nearest coupon schema"""

from dataclasses import dataclass, field


@dataclass
class NearestCouponSchema:
    """Nearest coupon schema"""

    date: str = field(default_factory=str)
    money_value: int = field(default_factory=int)
