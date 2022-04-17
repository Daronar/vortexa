from datetime import datetime
from typing import Any, Callable, Optional

import os


def get_env(name: str, default: Optional[Any] = None, cast: Callable = lambda x: x):
    value = os.getenv(name)
    if value is None:
        return default
    if cast is bool:
        lower_value = value.lower()
        if lower_value in ('yes', 'true', '1'):
            return True
        if lower_value in ('no', 'false', '0'):
            return False
    else:
        return cast(value)


class Config:
    """
        Class to store settings from ENV variables.
    """
    LOG_LEVEL = get_env('LOG_LEVEL', 'DEBUG', cast=str.strip)
    # Datetime to which we want to check the updates of ports. None - for handling every event
    MAX_DATETIME = get_env(
        'MAX_DATETIME',
        default='14/01/2020 00:00:00',
        cast=lambda x: datetime.strptime(x, '%d/%m/%Y %H:%M:%S') if x else None
    )
    PATH_TO_PORTS_FILE = get_env('PATH_TO_PORT_FILE', default='data/storage_asof_20200101.parquet', cast=str.strip)
    PATH_TO_EVENT_FILE = get_env('PATH_TO_EVENT_FILE', default='data/cargo_movements.parquet', cast=str.strip)
    USE_MULTIPROCESSING = get_env('USE_MULTIPROCESSING', default=False, cast=bool)
    PATH_TO_RESULT_FILE = get_env('PATH_TO_RESULT_FILE', default='./storage_asof_20200114.csv', cast=str.strip)
