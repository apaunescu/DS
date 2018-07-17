import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import gzip
import difflib
import sys
import datetime
import time
from scipy import stats

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

weekends = weekends.dropna()
weekdays = weekdays.dropna()

weekdays = weekdays.reset_index(drop = True)
weekends = weekends.reset_index(drop = True)

print(stats.ttest_ind(weekdays['comment_count'], weekends['comment_count']))

#x = np.concatenate((weekdays['comment_count'], weekends['comment_count']))
print(stats.normaltest(weekdays['comment_count']))
print(stats.normaltest(weekends['comment_count']))
print(stats.levene(weekdays['comment_count'], weekends['comment_count']))

print(stats.normaltest(np.sqrt(weekdays['comment_count'])))
print(stats.normaltest(np.sqrt(weekends['comment_count'])))
print(stats.levene(np.sqrt(weekdays['comment_count']), np.log(weekends['comment_count'])))

weekendpair = pd.DataFrame(data = weekends)
weekdaypair = pd.DataFrame(data = weekdays)
#weekends.isocalendar()

#https://stackoverflow.com/questions/29917931/python-define-starting-day-in-week-definition-in-isocalendar-or-strftime-or-els
weekendpair['date'] = weekends['date'].apply(lambda x: str(x.isocalendar()[0]) + "/" + str(x.isocalendar()[1]))
weekdaypair['date'] = weekdays['date'].apply(lambda x: str(x.isocalendar()[0]) + "/" + str(x.isocalendar()[1]))

weekendpair = weekendpair.groupby('date').mean().reset_index()
weekdaypair = weekdaypair.groupby('date').mean().reset_index()

print(stats.normaltest(weekendpair['comment_count']))
print(stats.normaltest(weekdaypair['comment_count']))

print(stats.ttest_ind(weekendpair['comment_count'], weekdaypair['comment_count']))

print(stats.mannwhitneyu(weekdays['comment_count'], weekends['comment_count']))
#print(weekendpair)
#print(weekdaypair)






plt.hist(np.log(weekdays['comment_count']), bins = 'auto')
#plt.hist(np.log(weekends['comment_count']), bins = 'auto')
plt.show()




#print(weekends)
#print(weekdays)


#weekends = pd.DataFrame(data = counts)
#weekends['date'] = counts['date']
#weekends['date'] = weekends['date'].apply(filterWeekend)


#.apply(filterWeekend)
#weekdays['date'] = counts['date'].apply(filterWeekday)