from utils import stock_price
from yahoo_finance_api2 import share

bikeou_instance = stock_price.StockPriceUtil(3377)
stock_price = bikeou_instance.get_stock_price(share.PERIOD_TYPE_MONTH, 1, share.FREQUENCY_TYPE_DAY, 1)

print(stock_price)