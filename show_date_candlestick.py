import matplotlib as mpl
mpl.use('TkAgg')

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc

from datetime import datetime
from dateutil.relativedelta import relativedelta

from mongoengine import *
from models import *

import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('all_dates', action = 'store')
results = parser.parse_args()

db_client = connect('stocks_db')

symbol = 'INFY'

all_dates = results.all_dates
all_dates = all_dates.split(',')
for marubozu_date in all_dates:
  marubozu_date = datetime.strptime(marubozu_date, '%Y-%m-%d')
  start_date = marubozu_date + relativedelta(months = -2)
  start_date = datetime.strptime(start_date.strftime('%Y-%m-%d'), '%Y-%m-%d')

  end_date = marubozu_date + relativedelta(months = 2)
  end_date = datetime.strptime(end_date.strftime('%Y-%m-%d'), '%Y-%m-%d')

  # First get the data from the database
  ohlc_data = []
  for sp in StockPrice.objects(symbol = symbol).order_by('date'):
    if start_date and sp.date < start_date: continue
    if end_date and sp.date > end_date: continue
    append_data = mdates.date2num(sp.date), sp.open, sp.high, sp.low, sp.close, sp.volume
    ohlc_data.append(append_data)

  # Then draw the data
  fig = plt.figure()
  ax1 = plt.subplot2grid((1, 1), (0, 0))

  candlestick_ohlc(ax1, ohlc_data, width = 0.5, colorup = 'blue', colordown = 'red')

  for label in ax1.xaxis.get_ticklabels():
    label.set_rotation(45)

  ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d %b, %y'))
  ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))

  xticks = ax1.get_xticks()
  xticks = np.append(xticks, [mdates.date2num(marubozu_date)])
  xticks = sorted(xticks)

  ax1.axvline(x = mdates.date2num(marubozu_date), alpha = 1, color = 'green',
    linestyle = 'dashed', linewidth = 0.3, ymin = 0, ymax = 0.15)

  ax1.xaxis.set_ticks(xticks)

  plt.xlabel('Date')
  plt.ylabel('Price')
  plt.title(symbol)
  plt.legend()
  plt.subplots_adjust(left = 0.09, bottom = 0.20, right = 0.94, top = 0.90, wspace = 0.2, hspace = 0)
  plt.show()

db_client.close()