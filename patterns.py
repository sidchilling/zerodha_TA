# This file has functions to return candlestick patterns found in data
from datetime import datetime
from dateutil.relativedelta import relativedelta

def _is_datapoint_ok(d):
  if d.get('open', None) and d.get('high', None) and d.get('low', None) and d.get('close', None) and d.get('volume', None):
    return True
  return False

def bullish_marubozu(data, low_range_percent = 1, high_range_percent = 10, shadow_points = 2):
  res = []
  for d in data:
    if not _is_datapoint_ok(d): continue
    if d.get('close') < d.get('open'): continue
    current_range_percent = ((d.get('close') - d.get('open')) * 100) / d.get('open')
    if current_range_percent < low_range_percent: continue
    if current_range_percent > high_range_percent: continue
    if d.get('low') < (d.get('open') - shadow_points): continue
    if d.get('high') > (d.get('close') + shadow_points): continue
    d['stoploss'] = d.get('low')
    res.append(d)
  return res

def bearish_marubozu(data, low_range_percent = 1, high_range_percent = 10, shadow_points = 2):
  res = []
  for d in data:
    if not _is_datapoint_ok(d): continue
    if d.get('close') > d.get('open'): continue
    current_range_percent = ((d.get('open') - d.get('close')) * 100) / d.get('close')
    if current_range_percent < low_range_percent: continue
    if current_range_percent > high_range_percent: continue
    if d.get('low') < (d.get('close') - shadow_points): continue
    if d.get('high') > (d.get('open') + shadow_points): continue
    d['stoploss'] = d.get('high')
    res.append(d)
  return res

def _is_date_spinning_top(d, max_range_percent, max_shadow_diff_percent):
  range_percent = (abs(d.get('open') - d.get('close')) * 100) / min(d.get('open'), d.get('close'))
  if range_percent > max_range_percent: return False
  high_shadow = d.get('high') - max(d.get('open'), d.get('close'))
  low_shadow = min(d.get('open'), d.get('close')) - d.get('low')
  shadow_diff_percent = (abs(high_shadow - low_shadow) * 100) / max(high_shadow, low_shadow)
  if shadow_diff_percent > max_shadow_diff_percent: return False
  return True

def spinning_tops(data, max_range_percent = 1, max_shadow_diff_percent = 70, backlook_trend_days = 10, min_trend_percent = 5):
  res = []
  index = -1
  for d in data:
    index = index + 1
    if not _is_datapoint_ok(d): continue
    if not _is_date_spinning_top(d, max_range_percent, max_shadow_diff_percent): continue
    prev_five_days_data = data[index - 5 : index]
    num_spinning_tops_found = 0
    for prev_d in prev_five_days_data:
      if _is_date_spinning_top(prev_d, max_range_percent, max_shadow_diff_percent):
        num_spinning_tops_found = num_spinning_tops_found + 1
    if num_spinning_tops_found > 2:
      # is there a trend
      current_median_price = min(d.get('open'), d.get('close')) + (abs(d.get('open') - d.get('close')) / 2.0)
      prev_day_index = index - backlook_trend_days
      if prev_day_index < 0:
        prev_day_index = 0
      prev_d = data[prev_day_index]
      prev_median_price = min(prev_d.get('open'), prev_d.get('close')) + (abs(prev_d.get('open') - prev_d.get('close')) / 2.0)
      trend_percent = (abs(current_median_price - prev_median_price) * 100) / prev_median_price
      if trend_percent >= min_trend_percent:
        res.append(d) 
  return res

def hammer(data, max_range_percent = 1, max_upper_shadow_points = 2, min_shadow_body_ratio = 2, backlook_trend_days = 10, min_trend_percent = 5):
  res = []
  index = -1
  for d in data:
    index = index + 1
    if not _is_datapoint_ok(d): continue
    # it should have a small real body
    range_percent = (abs(d.get('open') - d.get('close')) * 100) / min(d.get('open'), d.get('close'))
    if range_percent > max_range_percent: continue
    upper_shadow_points = d.get('high') - max(d.get('open'), d.get('close'))
    if upper_shadow_points > max_upper_shadow_points: continue
    range = abs(d.get('open') - d.get('close'))
    lower_shadow_range = min(d.get('open'), d.get('close')) - d.get('low')
    if (range * min_shadow_body_ratio) > lower_shadow_range: continue
    current_median_price = min(d.get('open'), d.get('close')) + (abs(d.get('open') - d.get('close')) / 2.0)
    prev_day_index = index - backlook_trend_days
    if prev_day_index < 0:
      prev_day_index = 0
    prev_d = data[prev_day_index]
    prev_median_price = min(prev_d.get('open'), prev_d.get('close')) + (abs(prev_d.get('open') - prev_d.get('close')) / 2.0)
    if prev_median_price < current_median_price: continue # hammer is in downtrend
    trend_percent = (abs(current_median_price - prev_median_price) * 100) / prev_median_price
    if trend_percent < min_trend_percent: continue
    res.append(d)      
  return res

def hanging_man(data, max_range_percent = 1, max_upper_shadow_points = 2, min_shadow_body_ratio = 2, backlook_trend_days = 10, min_tend_percent = 5):
  res = []
  index = -1
  for d in data:
    index = index + 1
    if not _is_datapoint_ok(d): continue
    range_percent = (abs(d.get('open') - d.get('close')) * 100) / min(d.get('open'), d.get('close'))
    if range_percent > max_range_percent: continue
    upper_shadow_points = d.get('high') - max(d.get('open'), d.get('close'))
    if upper_shadow_points > max_upper_shadow_points: continue
    range = abs(d.get('open') - d.get('close'))
    lower_shadow_range = min(d.get('open'), d.get('close')) - d.get('low')
    if (range * min_shadow_body_ratio) > lower_shadow_range: continue
    current_median_price = min(d.get('open'), d.get('close')) + (abs(d.get('open') - d.get('close')) / 2.0)
    prev_day_index = index - backlook_trend_days
    if prev_day_index < 0:
      prev_day_index = 0
    prev_d = data[prev_day_index]
    prev_median_price = min(prev_d.get('open'), prev_d.get('close')) + (abs(prev_d.get('open') - prev_d.get('close')) / 2.0)
    if prev_median_price > current_median_price: continue
    trend_percent = (abs(current_median_price - prev_median_price) * 100) / prev_median_price
    if trend_percent < min_tend_percent: continue
    res.append(d)
  return res