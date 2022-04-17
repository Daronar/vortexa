from abc import ABC, abstractmethod
from typing import Dict


class BaseEventGenerator(ABC):
    """
    Abstract class to generate JSON events.
    It could be not only from file but from HTTP API too.
    """
    @abstractmethod
    def __next__(self) -> Dict:
        raise NotImplemented()

    @abstractmethod
    def __iter__(self):
        raise NotImplemented()
