from typing import List
import numpy as np
import pandas as pd


FIELDS_MAP = {
    'internal_supply': 1,
    'external_supply': 2,
    'consumption': 3,
    'feed-in': 4,
    'self-consumption': 5,
    'generation': 6,
}

class DataParser():

    _header: List[str]

    def __init__(self):
        self.__header = []
        self._data = []

    def parse(self, file_name: str):
        self._data = pd.read_csv(file_name, delimiter=';', thousands=',')
        self._header = self._data.columns

    def data_by_time_and_field(self, timestamp: float, field: str) -> float:
        index = int(timestamp * 4) - 1
        return self._data[self._header[FIELDS_MAP[field]]][index]

    def data_by_field(self, field: str) -> np.ndarray:
        return self._data[self._header[FIELDS_MAP[field]]].to_numpy()

    def data_by_fields(self, fields: List[str]) -> np.ndarray:
        data_list = []
        for field in fields:
            data_list.append(self.data_by_field(field))
        return np.array(data_list).transpose()

    def get_times(self) -> List[float]:
        return [f"{i//4}" for i in range(24*4)]

    @property
    def header(self) -> List[str]:
        return _header
