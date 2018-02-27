import patterns as patterns
import utils as utils

symbol = 'INFY'
data = utils.get_symbol_data(symbol = symbol)
marubozus = patterns.bearish_marubozu(data = data)
dates = [d.get('date').strftime('%Y-%m-%d') for d in marubozus]
print 'Dates: {}'.format(dates)