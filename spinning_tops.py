import patterns as patterns
import utils as utils

symbol = 'INFY'
data = utils.get_symbol_data(symbol = symbol)
spinning_tops = patterns.spinning_tops(data = data)
dates = [d.get('date').strftime('%Y-%m-%d') for d in spinning_tops]
print 'Dates: {}'.format(dates)