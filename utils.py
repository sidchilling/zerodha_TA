from mongoengine import *
from models import *

def get_symbol_data(symbol):
  db_client = connect(db = 'stocks_db')
  data = []
  for sp in StockPrice.objects(symbol = symbol).order_by('date'):
    data.append({
      'date': sp.date,
      'open': sp.open,
      'high': sp.high,
      'low': sp.low,
      'close': sp.close,
      'volume': sp.volume
    })
  db_client.close()
  return data