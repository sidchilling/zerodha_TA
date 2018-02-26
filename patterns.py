# This file has functions to return candlestick patterns found in data

def bullish_marubozu(data, low_range_percent = 1, high_range_percent = 10, shadow_points = 2):
  res = []
  for d in data:
    if not d.get('open', None) or not d.get('high', None) or not d.get('low', None) or not d.get('close', None):
      continue
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
    if not d.get('open', None) or not d.get('high', None) or not d.get('low', None) or not d.get('close', None):
      continue
    if d.get('close') > d.get('open'): continue
    current_range_percent = ((d.get('open') - d.get('close')) * 100) / d.get('close')
    if current_range_percent < low_range_percent: continue
    if current_range_percent > high_range_percent: continue
    if d.get('low') < (d.get('close') - shadow_points): continue
    if d.get('high') > (d.get('open') + shadow_points): continue
    d['stoploss'] = d.get('high')
    res.append(d)
  return res