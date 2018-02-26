from mongoengine import *

class StockPrice(Document):
  symbol = StringField(required = True)
  date = DateTimeField(required = True)
  open = FloatField(required = True)
  high = FloatField(required = True)
  low = FloatField(required = True)
  close = FloatField(required = True)
  volume = IntField(required = True)
