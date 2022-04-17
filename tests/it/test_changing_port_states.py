from datetime import datetime, timedelta

import pandas as pd
import pytest

from src.events.types import Event
from src.event_generators.file_event_generator import ParquetEventGenerator
from src.event_handlers.port_event_handler import PortEventHandler
from src.resources.serializer import PortsSerializer, PortsReader

from tests.utils import generate_ports, generate_events, generate_full_result_ports, generate_partial_result_ports


@pytest.fixture
def ports_dataframe() -> pd.DataFrame:
    yield generate_ports()


@pytest.fixture
def events_dataframe() -> pd.DataFrame:
    yield generate_events()


class TestChangingPortStates:
    @staticmethod
    def assert_result(result: pd.DataFrame, expected: pd.DataFrame):
        for column in result.columns:
            assert all(result[column] == expected[column])

    @pytest.mark.parametrize('full_period', [True, False])
    def test_events_handling_in_single_process(self, ports_dataframe, events_dataframe, full_period):
        event_generator = ParquetEventGenerator(
            dataframe=events_dataframe,
            max_datetime=None if full_period else datetime.now() - timedelta(days=6),
        )
        ports = PortsReader.read_ports_from_dataframe(
            dataframe=ports_dataframe,
        )
        event_handler = PortEventHandler(
            ports=ports,
        )
        for raw_event in event_generator:
            event_handler.handle_event(event=Event(**raw_event))

        expected_result = generate_full_result_ports() if full_period else generate_partial_result_ports()
        serialized_ports = PortsSerializer.serialize(event_handler.ports)

        self.assert_result(
            result=serialized_ports,
            expected=expected_result
        )
