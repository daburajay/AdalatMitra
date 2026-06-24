"""
models/order_model.py
Defines the shape of a single court order/hearing record.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class OrderModel:
    """A single order/hearing entry for a case."""

    order_date: str = "N/A"
    order_type: str = "N/A"
    judge: str = "N/A"
    pdf_url: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "order_date": self.order_date,
            "order_type": self.order_type,
            "judge": self.judge,
            "pdf_url": self.pdf_url,
        }
