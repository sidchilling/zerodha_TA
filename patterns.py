# This file has functions to return candlestick patterns found in data

def bullish_marubozu(data, range_percent = 1, shadow_points = 2):
  res = []
  for d in data:
    if not d.get('open', None) or not d.get('high', None) or not d.get('low', None) or not d.get('close', None):
      continue
    if d.get('close') < d.get('open'): continue
    current_range_percent = ((d.get('close') - d.get('open')) * 100) / d.get('open')
    if current_range_percent < range_percent: continue
    if d.get('low') < (d.get('open') - shadow_points): continue
    if d.get('high') > (d.get('close') + shadow_points): continue
    res.append(d)
  return res