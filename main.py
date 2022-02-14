from utils import finance
from utils import stock_price
from utils import dataframe
from yahoo_finance_api2 import share
import pandas as pd
import numpy as np

# 株価を取得
bikeou_instance = finance.StockPriceUtil(3377)
data = bikeou_instance.get_stock_price(share.PERIOD_TYPE_YEAR, 1, share.FREQUENCY_TYPE_DAY, 1)

# データフレームに変換
df = pd.DataFrame(data)
df = dataframe.initialize_columns(df)
df[dataframe.T_CLOSE] = df[dataframe.CLOSE].shift(-1)
df[dataframe.SMA_5] = stock_price.sma(df, 5)
df[dataframe.SMA_25] = stock_price.sma(df, 25)
df[dataframe.SMA_75] = stock_price.sma(df, 75)
df[dataframe.GC_S_M] = stock_price.gc_s_m(df).astype(dtype="int")
df[dataframe.GC_S_L] = stock_price.gc_s_l(df).astype(dtype="int")
df[dataframe.DC_S_M] = stock_price.dc_s_m(df).astype(dtype="int")
df[dataframe.DC_S_L] = stock_price.dc_s_l(df).astype(dtype="int")

df = df.fillna(0) # 欠損値NaNを0で置き換え
predict_data = df[len(df)-1:len(df)]
df = df[0:len(df)-1] # 最後の行はpredictで使用するので除外

# 説明変数と検証用データと目的変数を取得
x: np.ndarray = df.drop(dataframe.T_CLOSE, axis=1).values
predict_x: np.ndarray = predict_data.drop(dataframe.T_CLOSE, axis=1).values
t: np.ndarray = df[dataframe.T_CLOSE].values