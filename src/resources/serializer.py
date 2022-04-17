from typing import List

import pandas as pd

from src.resources.port import Port
from src.events.types import ProductType
from src.resources.product_storage import ProductStorage


class PortsSerializer:
    """
        Serialize ports to pandas DataFrame
    """
    @staticmethod
    def serialize(ports: List[Port]) -> pd.DataFrame:
        columns = ['port']
        for product_type in ProductType:
            if product_type == ProductType.UNKNOWN:
                continue
            columns.extend([f'{product_type.value}_absolute', f'{product_type.value}_relative'])
        return pd.DataFrame(
            data=[
                port.serialize() for port in ports
            ],
            columns=columns
        ).rename(columns={'crude oil_absolute': 'crude_absolute', 'crude oil_relative': 'crude_relative'})


class PortsReader:
    """
        Read ports and its storages from parquet file.
    """
    @classmethod
    def read_ports_from_dataframe(cls, dataframe: pd.DataFrame):
        ports = []
        for _, row in dataframe.iterrows():
            oil_storage = ProductStorage(
                product_type=ProductType.CRUDE_OIL,
                current=row['crude_absolute'],
                relative=row['crude_relative'],
            )
            diesel_storage = ProductStorage(
                product_type=ProductType.DIESEL,
                current=row['diesel_absolute'],
                relative=row['diesel_relative'],
            )
            ports.append(
                Port(
                    name=row['port'],
                    product_storages=[oil_storage, diesel_storage],
                )
            )
        return ports
