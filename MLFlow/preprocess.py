import numpy as np
import pandas as pd
import yfinance as yf
from ta.trend import MACD
import gym
from gym import spaces
import matplotlib.pyplot as plt
import math

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


def process_data(ticker, start, end, real_start):
    data = yf.download(ticker, start=start, end=end).reset_index()
    data['macd'] = MACD(data['Close']).macd()
    data['obv'] = calculate_obv(data)
    data['price_next_day'] = data.loc[1:,'Open'].reset_index(drop = True)
    data = data[(data['Date'] >= real_start) & ~(data['price_next_day'].isna())].reset_index(drop = True)
    return data