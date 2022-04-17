from typing import Dict, List

import logging

from src.resources.port import Port
from src.events.types import ActionType, ProductType, Event

logger = logging.getLogger(__name__)


class PortEventHandler:
    """
        Handle event and change state of event port
    """
    _ports: Dict[str, Port]

    counter: int = 0

    def __init__(self, ports: List[Port]):
        self._ports = {
            port.name: port
            for port in ports
        }

    @property
    def ports(self) -> List[Port]:
        return list(self._ports.values())

    def handle_event(self, event: Event) -> None:
        logger.debug(f'Get event {event}.')
        if event.product == ProductType.UNKNOWN or event.action == ActionType.UNKNOWN:
            logger.debug(f'Skip event {event}. Reason: unknown type of product.')
            return

        if event.port not in self._ports:
            logger.debug(f'Skip event {event}. Reason: unobserved port {event.port}.')
            return

        port = self._ports[event.port]
        if event.product not in port.product_storages:
            logger.debug(f'Skip event {event}. Reason: unobserved product {event.product} for port {port.name}.')
            return

        if event.action == ActionType.LOAD:
            port.sub_product(product_type=event.product, amount=event.quantity)
        elif event.action == ActionType.DISCHARGE:
            port.add_product(product_type=event.product, amount=event.quantity)
        else:
            logger.debug(f'Skip event {event}. Reason: invalid type of action.')

        self.counter += 1
        logger.debug(f'Successful handled event {event}.')

