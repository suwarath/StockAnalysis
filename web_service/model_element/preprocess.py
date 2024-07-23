import numpy as np
import pandas as pd
import yfinance as yf
from ta.trend import MACD
import datetime as dt

def calculate_obv(df):
        obv = [0] * len(df)
        for i in range(1, len(df)):
            if df['Close'][i] > df['Close'][i - 1]:
                obv[i] = obv[i - 1] + df['Volume'][i]
            elif df['Close'][i] < df['Close'][i - 1]:
                obv[i] = obv[i - 1] - df['Volume'][i]
            else:
                obv[i] = obv[i - 1]
        return np.array(obv)


def process_data(ticker, start, end):
    download_start = (dt.datetime.strptime(start, "%Y-%m-%d") - dt.timedelta(days = 60)).strftime('%Y-%m-%d')
    data = yf.download(ticker, start=download_start, end=end).reset_index()
    data['macd'] = MACD(data['Close']).macd()
    data['macd_signal'] = MACD(data['Close']).macd_signal()
    data['macd_diff'] = MACD(data['Close']).macd_diff()
    data['obv'] = calculate_obv(data)
    data['price_next_day'] = data.loc[1:,'Open'].reset_index(drop = True)
    data = data[(data['Date'] >= start) & ~(data['price_next_day'].isna())].reset_index(drop = True)
    return data