from mongoengine import *
from models import *
import patterns as patterns

db_client = connect(db = 'stocks_db')

symbol = 'INFY'
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

marubozus = patterns.bullish_marubozu(data = data)
marubozu_dates = [d.get('date').strftime('%Y-%m-%d') for d in marubozus]
print 'Dates: {}'.format(marubozu_dates)

db_client.close()
