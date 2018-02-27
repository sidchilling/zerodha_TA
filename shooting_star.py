import patterns as patterns
import utils as utils

symbol = 'INFY'
data = utils.get_symbol_data(symbol = symbol)

res = patterns.shooting_star(data = data)
dates = [d.get('date').strftime('%Y-%m-%d') for d in res]

print dates