from typing import List

import unittest

from src.resources.port import Port
from src.resources.product_storage import ProductStorage
from src.resources.serializer import PortsSerializer
from src.events.types import ProductType


class TestPortsSerializer(unittest.TestCase):
    @staticmethod
    def prepare_ports() -> List[Port]:
        ports = []
        for port_name in ['test_port_1', 'test_port_2']:
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
            ports.append(
                Port(name=port_name, product_storages=[storage1, storage2])
            )
        return ports

    def test_ports_serialize(self):
        ports = self.prepare_ports()
        serialized_ports = PortsSerializer.serialize(ports)

        assert serialized_ports.shape[0] == 2
        columns = ['port', 'crude_absolute', 'crude_relative', 'diesel_absolute', 'diesel_relative']
        assert list(serialized_ports.columns) == columns
