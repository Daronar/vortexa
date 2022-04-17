import unittest

from src.resources.product_storage import ProductStorage, UNKNOWN_STORAGE_SIZE
from src.events.types import ProductType


class TestProductStorage(unittest.TestCase):
    def test_product_storage(self):
        storage = ProductStorage(
            product_type=ProductType.CRUDE_OIL,
            current=10,
            relative=0.1,
        )
        assert storage.total == 100
        assert storage.type == ProductType.CRUDE_OIL
        assert storage.current == 10

        storage.add_product(amount=30)

        assert storage.total == 100
        assert storage.type == ProductType.CRUDE_OIL
        assert storage.current == 40

    def test_zero_init_product_storage(self):
        storage = ProductStorage(
            product_type=ProductType.CRUDE_OIL,
            current=0,
            relative=0,
        )
        assert storage.total == UNKNOWN_STORAGE_SIZE
        assert storage.type == ProductType.CRUDE_OIL
        assert storage.current == 0

