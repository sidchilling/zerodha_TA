import patterns as patterns
import utils as utils

symbol = 'INFY'
data = utils.get_symbol_data(symbol = symbol)
marubozus = patterns.bullish_marubozu(data = data)
marubozu_dates = [d.get('date').strftime('%Y-%m-%d') for d in marubozus]
print 'Dates: {}'.format(marubozu_dates)
