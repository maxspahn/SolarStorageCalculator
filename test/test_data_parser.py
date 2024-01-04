import pytest
import numpy as np
from solarcalc.helpers import DataParser

def test_data_parser():
    dp = DataParser()
    dp.parse('data/20240101.csv')
    value = dp.data_by_time_and_field(9.5, 'internal_supply')
    assert value == 89
    value = dp.data_by_time_and_field(12.25, 'generation')
    assert value == 1305
    values_day = dp.data_by_field('internal_supply')
    assert isinstance(values_day, np.ndarray)
    values_day = dp.data_by_fields(['internal_supply', 'external_supply'])
    assert isinstance(values_day, np.ndarray)
    assert values_day.shape[1] == 2
    assert dp.interval == 0.25
    assert dp.length == 96
    
