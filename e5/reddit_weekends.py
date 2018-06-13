import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import gzip
import difflib
import sys
import datetime
import scipy

counts = pd.read_json(sys.argv[1], lines=True)
counts['date'] = pd.to_datetime(counts['date'])

def filterWeekend(date):
	if (date.weekday() == 5) or (date.weekday() == 6):
		return date
	return np.NaN

def filterWeekday(date):
	if (date.weekday() == 5) or (date.weekday() == 6):
		return np.NaN
	return date

def filterCanada(subreddit):
	if (subreddit != 'canada'):
		return np.NaN
	return subreddit

counts = counts[(counts['date'].dt.year >= 2012) & (counts['date'].dt.year <= 2013)]
counts['subreddit'] = counts['subreddit'].apply(filterCanada)
weekends = counts[(counts['date'].dt.weekday == 5) | (counts['date'].dt.weekday == 6)]


weekdays = pd.DataFrame(data = counts)
weekdays['date'] = counts['date']
weekdays['date'] = weekdays['date'].apply(filterWeekday)

#weekends = pd.DataFrame(data = counts)
#weekends['date'] = counts['date']
#weekends['date'] = weekends['date'].apply(filterWeekend)


#.apply(filterWeekend)
#weekdays['date'] = counts['date'].apply(filterWeekday)


weekends = weekends.dropna()
weekdays = weekdays.dropna()


print(weekends)
print(weekdays)