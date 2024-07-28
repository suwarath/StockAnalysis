import sys

import requests

sys.path.append("./web_service")
from model_element.model import parameters


def test_docker():
    ticker_info = {"ticker": "AAPL", "target_date": "2024-01-05"}

    url = "http://localhost:9696/get_action"

    actual_response = requests.post(url, json=ticker_info, timeout=60).json()

    if parameters == ["Close", "macd", "macd_diff", "macd_signal", "obv"]:
        expected_response_parm_dict = str(
            {
                "Close": 181.17999267578125,
                "macd": -1.527435403503489,
                "macd_diff": -1.972018625858581,
                "macd_signal": 0.44458322235509207,
                "obv": -52485900,
            }
        )
        expected_response_target_date = "2024-01-05"
    elif parameters == ["Close", "Volume", "macd", "obv"]:
        expected_response_parm_dict = str(
            {
                "Close": 181.17999267578125,
                "Volume": 62303300,
                "macd": -1.527435403503489,
                "obv": -52485900,
            }
        )
        expected_response_target_date = "2024-01-05"

    assert (
        expected_response_parm_dict == actual_response["parm_dict"]
    ), "parm_dict error"
    assert (
        expected_response_target_date == actual_response["target_date"]
    ), "target_date error"
