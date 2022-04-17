from datetime import datetime
from typing import Iterator, Dict, Optional

import pandas as pd

from src.event_generators.base_event_generator import BaseEventGenerator


class ParquetEventGenerator(BaseEventGenerator):
    _df: pd.DataFrame

    _df_iter: Iterator

    def __init__(self, dataframe: pd.DataFrame, max_datetime: Optional[datetime] = None):
        event_df = dataframe
        loading_df = event_df.loc[:, ['loading_port', 'start_timestamp', 'product', 'quantity']].rename(
            columns={'start_timestamp': 'ts', 'loading_port': 'port'}
        )
        loading_df['action'] = 'load'

        discharge_df = event_df.loc[:, ['discharge_port', 'end_timestamp', 'product', 'quantity']].rename(
            columns={'end_timestamp': 'ts', 'discharge_port': 'port'}
        )
        discharge_df['action'] = 'discharge'

        self._df = pd.concat([loading_df, discharge_df]).sort_values('ts')

        if max_datetime:
            self._df = self._df[self._df['ts'] <= max_datetime]

    def __iter__(self) -> 'ParquetEventGenerator':
        self._df_iter = self._df.iterrows()
        return self

    def __next__(self) -> Dict:
        _, raw_event = next(self._df_iter)
        return raw_event.to_dict()
