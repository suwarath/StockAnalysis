import sys

import numpy as np
import pandas as pd

sys.path.append("./web_service")
from model_element.preprocess import (  # type: ignore
    process_data,
    calculate_obv
)


def test_calculate_obv():
    """1. test calculate obv function"""
    data_input = {"Close": [10, 20, 15, 15], "Volume": [100, 200, 150, 100]}
    test_input = pd.DataFrame(data_input)
    expected_output = np.array([0, 200, 50, 50])

    actual_output = calculate_obv(test_input)

    assert (expected_output != actual_output).sum() == 0, "Calculate obv error"


def test_pre_process_data():
    """2. Test Downloaded data from yahoo finance
    which should not have any NA value in any columns"""

    test_ticker = "AAPL"
    test_start = "2023-06-01"
    test_end = "2023-07-01"

    actual_output = (
        process_data(test_ticker, test_start, test_end).isnull().any().sum()
    )

    assert actual_output == 0, "Preprocess Error - Has null value(s)"
