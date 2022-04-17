from src.events.types import ProductType


UNKNOWN_STORAGE_SIZE = 100000000


class ProductStorage:
    """
        Control product storage.
    """
    type: ProductType

    current: int
    total: int

    def __init__(self, product_type: ProductType, current: int, relative: float):
        self.type = product_type
        self.current = current
        if current > 0:
            self.total = int(current / relative)
        else:
            self.total = UNKNOWN_STORAGE_SIZE

    @property
    def relative(self) -> float:
        return self.current / self.total

    def __repr__(self) -> str:
        return f'{{product_type={self.type}, current={self.current}}}'

    def add_product(self, amount: int) -> None:
        self.current += amount

    def sub_product(self, amount: int) -> None:
        self.current -= amount
