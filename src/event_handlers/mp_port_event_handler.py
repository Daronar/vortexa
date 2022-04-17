import time
from queue import Empty
from multiprocessing import Queue, TimeoutError
from typing import Dict

import logging

from src.event_handlers.port_event_handler import PortEventHandler
from src.events.types import Event

TIME_TO_SLEEP_AFTER_READING = 0.1
DEFAULT_RETRY_COUNT = 5

logger = logging.getLogger(__name__)


class RetryCountExhausted(Exception):
    """Retry count for getting data from queue"""


class MultiProcessingPortEventHandler:
    """
        Handle events and change port states.
        Run in separate process and get events from queue.
    """
    _q: Queue
    _event_handler: PortEventHandler
    _retry_count: int

    def __init__(
            self,
            event_handler: PortEventHandler,
            queue: Queue,
            retry_count: int = DEFAULT_RETRY_COUNT,
    ):
        super().__init__()
        self._event_handler = event_handler
        self._q = queue
        self._retry_count = retry_count

    def _read_event(self) -> Event:
        """
            Try to read event from queue.
            Sleep after every try.
            Retry for _retry_to_stop, if it is exhausted, stop reading.
        """
        for retry_count in range(self._retry_count):
            try:
                raw_event: Dict = self._q.get(timeout=TIME_TO_SLEEP_AFTER_READING)
                return Event(**raw_event)
            except TimeoutError:
                pass
            except Empty:
                pass
        raise RetryCountExhausted()

    def handle_events(self) -> None:
        logger.debug('Sleep waiting the initialization of generator processes.')
        time.sleep(0.5)
        try:
            while True:
                event = self._read_event()
                self._event_handler.handle_event(event=event)
        except RetryCountExhausted:
            logger.info('Retry count to read from queue count is expired. Stop reading from queue.')
