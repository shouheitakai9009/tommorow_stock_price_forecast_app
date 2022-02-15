from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError

class StockPriceUtil():
  def __init__(self, symbol: int):
    self.symbol = symbol

  def get_stock_price(self, period_type, period, frequency_type, frequency):
    symbol_data = {}
    my_self = share.Share(self.symbol)
    try:
      symbol_data = my_self.get_historical(period_type, period, frequency_type, frequency)
    except YahooFinanceError as e:
      print(e)
    return symbol_data