from typing import List
import re
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
    _interval: float
    _length: int

    def __init__(self):
        self._header = []
        self._data = []
        self._interval = 1.0
        self._length = 24 * 4

    def parse(self, file_name: str):
        self._data = pd.read_csv(file_name, delimiter=';', thousands=',')
        self._header = self._data.columns
        self._interval = int(re.split('"|:', self._data[self._header[0]][0])[2])/60
        self._length = self._data.shape[0]

    @property
    def length(self) -> int:
        return self._length

    @property
    def interval(self) -> float:
        return self._interval

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
        return [f"{i%24//4}" for i in range(self.length)]

    @property
    def header(self) -> List[str]:
        return _header

class Storage():
    _capacity: float
    _charge: List[float]
    _feed_in: List[float]
    _external: List[float]
    _interval: float
    _initial_charge: float

    def __init__(self, initial_charge: float, interval: float, capacity: float):
        self._charge = []
        self._feed_in = []
        self._external = []
        self._capacity = capacity
        self._interval = interval
        self._initial_charge = initial_charge


    def set_production_consumption(self, production: List[float], consumption: List[float]) -> None:
        assert len(production) == len(consumption)
        current_charge = self._initial_charge
        for i in range(len(production)):
            gained_charge = self._interval * (production[i] - consumption[i])
            current_charge += gained_charge
            external = max(0, 0 - current_charge)
            feed_in = max(0, current_charge - self._capacity)
            current_charge = min(self._capacity, current_charge)
            current_charge = max(0, current_charge)
            self._charge.append(current_charge)
            self._feed_in.append(feed_in/self._interval)
            self._external.append(external/self._interval)

    @property
    def charge(self) -> List[float]:
        return self._charge

    @property
    def feed_in(self) -> List[float]:
        return self._feed_in

    @property
    def sum_feed_in(self) -> float:
        return sum(self.feed_in) * self._interval

    @property
    def external(self) -> List[float]:
        return self._external

    @property
    def sum_external(self) -> float:
        return sum(self.external) * self._interval

