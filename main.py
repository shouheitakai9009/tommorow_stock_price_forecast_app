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
after_n_day: int = 1 # n日後を指定する変数
train_size: int = 0.5 # 100%のデータのうち、何％をトレーニングに回すか
instance = finance.StockPriceUtil("4689.T") # 銘柄コード
data = instance.get_stock_price(share.PERIOD_TYPE_YEAR, 5, share.FREQUENCY_TYPE_DAY, 1)

# 日経平均株価を取得
nikkei_instance = finance.StockPriceUtil("^N225") # 銘柄コード
nikkei_data = nikkei_instance.get_stock_price(share.PERIOD_TYPE_YEAR, 5, share.FREQUENCY_TYPE_DAY, 1)
df_nikkei = pd.DataFrame(nikkei_data)

# データフレームに変換
df = pd.DataFrame(data)
df = dataframe.initialize_columns(df)
df[dataframe.N_CLOSE] = df[dataframe.CLOSE].shift(-after_n_day)
df[dataframe.VOLATILITY] = stock_price.volatility(df)
df[dataframe.SMA_5] = stock_price.sma(df, 5)
df[dataframe.SMA_25] = stock_price.sma(df, 25)
df[dataframe.SMA_75] = stock_price.sma(df, 75)
df[dataframe.GC_S_M] = stock_price.gc_s_m(df).astype(dtype="int")
df[dataframe.GC_S_L] = stock_price.gc_s_l(df).astype(dtype="int")
df[dataframe.DC_S_M] = stock_price.dc_s_m(df).astype(dtype="int")
df[dataframe.DC_S_L] = stock_price.dc_s_l(df).astype(dtype="int")
df[dataframe.N225_CLOSE] = df_nikkei['close']
df[dataframe.N225_VOLUME] = df_nikkei['volume']

df = df.fillna(0) # 欠損値NaNを0で置き換え

# 説明変数と検証用データと目的変数を取得
x: np.ndarray = df.drop(dataframe.N_CLOSE, axis=1).values
t: np.ndarray = df[dataframe.N_CLOSE].values
x_train, x_test, t_train, t_test = train_test_split(x, t, train_size=train_size, random_state=0, shuffle=False)

# モデルの実装
model = LinearRegression()
model.fit(x_train, t_train)
score = model.score(x_test, t_test)
print(f'正解率は{np.round(score*100, decimals=2)}%でした。')

y = model.predict(x_test)
plt.figure(figsize=(20,10))
plt.plot(df['timestamp'], df[dataframe.CLOSE])
plt.plot(df['timestamp'][int(len(df) * train_size):len(df)], y)
# plt.show()

y_mean = y[len(y)-6:len(y)-1].mean()
t_test_mean = t_test[len(t_test)-after_n_day-5:len(t_test)-after_n_day].mean()
adj_add_price = t_test_mean - y_mean # テストデータと実値の乖離を調整する値

for i in range(0, after_n_day):
  stock_price = np.round(y[len(y)-(after_n_day - (i))] + adj_add_price,decimals=1)
  print(f"{i + 1}日後の株価は{stock_price}円になりそうです。")