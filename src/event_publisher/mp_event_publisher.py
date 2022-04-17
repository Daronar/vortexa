from multiprocessing import Process, Queue

import logging

from src.event_generators.base_event_generator import BaseEventGenerator

logger = logging.getLogger(__name__)


class MultiProcessingEventPublisher(Process):
    _q: Queue
    _event_generator: BaseEventGenerator

    def __init__(self, event_generator: BaseEventGenerator, queue: Queue):
        super().__init__()
        self._event_generator = event_generator
        self._q = queue

    def run(self) -> None:
        logger.debug(f'Start event publisher.')
        for event in self._event_generator:
            self._q.put(event)

