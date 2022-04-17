from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class ProductType(Enum):
    CRUDE_OIL = 'crude oil'
    DIESEL = 'diesel'
    UNKNOWN = 'unknown'

    @classmethod
    def _missing_(cls, value):
        return ProductType.UNKNOWN


class ActionType(Enum):
    LOAD = 'load'
    DISCHARGE = 'discharge'
    UNKNOWN = 'unknown'

    @classmethod
    def _missing_(cls, value):
        return ActionType.UNKNOWN


@dataclass
class Event:
    port: str
    quantity: int
    ts: datetime
    action: ActionType
    product: ProductType

    def __post_init__(self):
        self.action = ActionType(self.action)
        self.product = ProductType(self.product)
