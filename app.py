from multiprocessing import Queue
from typing import List

import logging
import pandas as pd

from src.config import Config
from src.events.types import Event
from src.event_generators.file_event_generator import ParquetEventGenerator
from src.event_publisher.mp_event_publisher import MultiProcessingEventPublisher
from src.event_handlers.mp_port_event_handler import MultiProcessingPortEventHandler
from src.event_handlers.port_event_handler import PortEventHandler
from src.resources.port import Port
from src.resources.serializer import PortsSerializer, PortsReader

config = Config()


def logger_init() -> logging.Logger:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(levelname)s: %(asctime)s - %(process)s - %(message)s"))
    logger = logging.getLogger()
    logger.setLevel(config.LOG_LEVEL)
    logger.addHandler(handler)
    return logger


logger = logger_init()


def single_process_handling(
    event_generator: ParquetEventGenerator,
    event_handler: PortEventHandler,
):
    for raw_event in event_generator:
        event_handler.handle_event(event=Event(**raw_event))


def multi_process_handling(
    event_generator: ParquetEventGenerator,
    event_handler: PortEventHandler,
):
    q = Queue(maxsize=1000)
    mp_event_publisher = MultiProcessingEventPublisher(
        event_generator=event_generator,
        queue=q,
    )
    mp_event_handler = MultiProcessingPortEventHandler(
        event_handler=event_handler,
        queue=q,
    )
    mp_event_publisher.start()
    mp_event_handler.handle_events()
    mp_event_publisher.join()


def main():
    event_generator = ParquetEventGenerator(
        dataframe=pd.read_parquet(config.PATH_TO_EVENT_FILE),
        max_datetime=config.MAX_DATETIME,
    )
    ports: List[Port] = PortsReader.read_ports_from_dataframe(
        dataframe=pd.read_parquet(config.PATH_TO_PORTS_FILE)
    )
    event_handler = PortEventHandler(
        ports=ports,
    )

    logger.info('Start handling events.')
    if config.USE_MULTIPROCESSING:
        multi_process_handling(event_generator=event_generator, event_handler=event_handler)
    else:
        single_process_handling(event_generator=event_generator, event_handler=event_handler)
    logger.info('Finish handling events.')

    logger.info(f'Dump port states to {config.PATH_TO_RESULT_FILE}.')
    serialized_ports = PortsSerializer.serialize(ports)
    serialized_ports.to_csv(path_or_buf=config.PATH_TO_RESULT_FILE)


if __name__ == '__main__':
    main()
