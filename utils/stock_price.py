import pandas as pd
from utils import dataframe

def volatility(df):
  return df[dataframe.HIGH] - df[dataframe.LOW]

# 単純移動平均を取得
def sma(df: pd.DataFrame, day: int):
  return df[dataframe.CLOSE].rolling(day).sum() / day

# 短期 >= 中期のゴールデンクロスを取得
def gc_s_m(df: pd.DataFrame):
  return df[dataframe.SMA_5] >= df[dataframe.SMA_25]

# 短期 >= 長期のゴールデンクロスを取得
def gc_s_l(df: pd.DataFrame):
  return df[dataframe.SMA_5] >= df[dataframe.SMA_75]

# 短期 < 中期のデッドクロスを取得
def dc_s_m(df: pd.DataFrame):
  return df[dataframe.SMA_5] < df[dataframe.SMA_25]

# 短期 < 長期のデッドクロスを取得
def dc_s_l(df: pd.DataFrame):
  return df[dataframe.SMA_5] < df[dataframe.SMA_75]