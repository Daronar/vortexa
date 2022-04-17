from typing import Tuple, List

import unittest

from src.resources.port import Port
from src.resources.product_storage import ProductStorage
from src.events.types import ProductType


class TestPort(unittest.TestCase):
    @staticmethod
    def prepare_port() -> Tuple[Port, List[ProductStorage]]:
        storage1 = ProductStorage(
            product_type=ProductType.CRUDE_OIL,
            current=10,
            relative=0.1,
        )
        storage2 = ProductStorage(
            product_type=ProductType.DIESEL,
            current=150,
            relative=0.2,
        )
        return Port(name='test_port', product_storages=[storage1, storage2]), [storage1, storage2]

    def test_port(self):
        port, storages = self.prepare_port()

        port.add_product(product_type=ProductType.CRUDE_OIL, amount=20)
        port.sub_product(product_type=ProductType.DIESEL, amount=30)

        assert storages[0].current == 30
        assert storages[0].total == 100

        assert storages[1].current == 120
        assert storages[1].total == 750

    def test_port_serialize(self):
        port, storages = self.prepare_port()
        serialized_port = port.serialize()

        assert len(serialized_port) == 5

        assert serialized_port[0] == port.name
        assert serialized_port[1] == storages[0].current
        assert serialized_port[2] == storages[0].relative
        assert serialized_port[3] == storages[1].current
        assert serialized_port[4] == storages[1].relative
