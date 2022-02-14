from utils import finance
from utils import stock_price
from utils import dataframe
from yahoo_finance_api2 import share
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 株価を取得
bikeou_instance = finance.StockPriceUtil(4689)
data = bikeou_instance.get_stock_price(share.PERIOD_TYPE_YEAR, 5, share.FREQUENCY_TYPE_DAY, 1)

# データフレームに変換
df = pd.DataFrame(data)
df = dataframe.initialize_columns(df)
df[dataframe.T_CLOSE] = df[dataframe.CLOSE].shift(-1)
df[dataframe.VOLATILITY] = stock_price.volatility(df)
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
x_train, x_test, t_train, t_test = train_test_split(x, t, test_size=0.3, random_state=0, shuffle=False)

# モデルの実装
model = LinearRegression()
model.fit(x_train, t_train)
score = model.score(x_test, t_test)
print(f'正解率は{np.round(score*100, decimals=2)}%でした。')

y = model.predict(predict_x)
print(f"次の日の株価は{y}円ですよ！")