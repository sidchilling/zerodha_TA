import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('all_dates', action = 'store')
results = parser.parse_args()

all_dates = results.all_dates
print all_dates