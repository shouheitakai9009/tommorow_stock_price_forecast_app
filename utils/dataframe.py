import pandas as pd

HIGH = "high" # 今日の高値
LOW = "low" # 今日の安値
CLOSE = "close" # 今日の終値
T_CLOSE = "t_close" # 翌営業日の終値
VOLATILITY = "volatility" # 価格変動の大きさ
SMA_5 = "sma5" # 5日単純移動平均
SMA_25 = "sma25" # 25日単純移動平均
SMA_75 = "sma75" # 75日単純移動平均
GC_S_M = "gc_s_m" # ゴールデンクロス（短期 >= 中期）
GC_S_L = "gc_s_l" # ゴールデンクロス（短期 >= 長期）
DC_S_L = "dc_s_l" # デッドクロス（短期 < 長期）
DC_S_M = "dc_s_m" # デッドクロス（短期 < 中期）

# Dataframeのカラム定義を初期化
def initialize_columns(df: pd.DataFrame):
  df[T_CLOSE] = 0
  df[VOLATILITY] = 0
  df[SMA_5] = 0
  df[SMA_25] = 0
  df[SMA_75] = 0
  df[GC_S_M] = 0
  df[GC_S_L] = 0
  df[DC_S_M] = 0
  df[DC_S_L] = 0
  return df