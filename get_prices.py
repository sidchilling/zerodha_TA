import nsepy
from datetime import date
from mongoengine import *
from models import *

db_client = connect(db = 'stocks_db')

start_date = date(2016, 2, 26)
end_date = date(2018, 2, 26)

symbol = 'INFY' # the stock whose price we have to get

data_df = nsepy.get_history(symbol = symbol, start = start_date, end = end_date)

for index, row in data_df.iterrows():
  date = index
  symbol = row['Symbol']
  open = row['Open']
  high = row['High']
  low = row['Low']
  close = row['Close']
  volume = row['Volume']
  print '{}, {}, {}, {}, {}, {}, {}'.format(symbol, date, open, high, low, close, volume)
  db_entry = StockPrice(symbol = symbol, date = date, open = open,
    high = high, low = low, close = close, volume = volume)
  db_entry.save()

db_client.close()