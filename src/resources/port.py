from typing import List, Dict

from src.events.types import ProductType
from src.resources.product_storage import ProductStorage


class Port:
    """
        Control port's storages of different product types.
    """
    name: str
    product_storages: Dict[ProductType, ProductStorage]

    def __init__(
            self,
            name: str,
            product_storages: List[ProductStorage]
    ):
        self.name = name
        self.product_storages = {
            product.type: product
            for product in product_storages
        }

    def serialize(self) -> List:
        serialized_port = [self.name]
        for product_type in ProductType:
            if product_type == ProductType.UNKNOWN:
                continue
            if product_type in self.product_storages:
                serialized_port.append(self.product_storages[product_type].current)
                serialized_port.append(self.product_storages[product_type].relative)
            else:
                serialized_port.extend([0, 0])
        return serialized_port

    def __repr__(self) -> str:
        return f'(name={self.name},storages=[{[str(storage) for storage in self.product_storages.values()]}])'

    def add_product(self, product_type: ProductType, amount: int) -> None:
        self.product_storages[product_type].add_product(amount)

    def sub_product(self, product_type: ProductType, amount: int) -> None:
        self.product_storages[product_type].sub_product(amount)
