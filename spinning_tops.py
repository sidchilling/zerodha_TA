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

spinning_tops = patterns.spinning_tops(data = data)
dates = [d.get('date').strftime('%Y-%m-%d') for d in spinning_tops]
print 'Dates: {}'.format(dates)

db_client.close()