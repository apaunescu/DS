import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import gzip
import difflib
import datetime
import time
from scipy import stats

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

OUTPUT_TEMPLATE = (
    "Initial (invalid) T-test p-value: {initial_ttest_p:.3g}\n"
    "Original data normality p-values: {initial_weekday_normality_p:.3g} {initial_weekend_normality_p:.3g}\n"
    "Original data equal-variance p-value: {initial_levene_p:.3g}\n"
    "Transformed data normality p-values: {transformed_weekday_normality_p:.3g} {transformed_weekend_normality_p:.3g}\n"
    "Transformed data equal-variance p-value: {transformed_levene_p:.3g}\n"
    "Weekly data normality p-values: {weekly_weekday_normality_p:.3g} {weekly_weekend_normality_p:.3g}\n"
    "Weekly data equal-variance p-value: {weekly_levene_p:.3g}\n"
    "Weekly T-test p-value: {weekly_ttest_p:.3g}\n"
    "Mann–Whitney U-test p-value: {utest_p:.3g}"
)


def main():
    reddit_counts = sys.argv[1]

    counts = pd.read_json(reddit_counts, lines=True)
    counts['date'] = pd.to_datetime(counts['date'])

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


    initialt = stats.ttest_ind(weekdays['comment_count'], weekends['comment_count'])[1]

    initialweekday = (stats.normaltest(weekdays['comment_count']))[1]
    initialweekend = (stats.normaltest(weekends['comment_count']))[1]

    initialLevene = (stats.levene(weekdays['comment_count'], weekends['comment_count']))[1]
    
    transformweekday = (stats.normaltest(np.sqrt(weekdays['comment_count'])))[1]
    transformweekend = (stats.normaltest(np.sqrt(weekends['comment_count'])))[1]

    transformLevene = (stats.levene(np.sqrt(weekdays['comment_count']), np.log(weekends['comment_count'])))[1]

    weekendpair = pd.DataFrame(data = weekends)
    weekdaypair = pd.DataFrame(data = weekdays)

    #https://stackoverflow.com/questions/29917931/python-define-starting-day-in-week-definition-in-isocalendar-or-strftime-or-els
    weekendpair['date'] = weekends['date'].apply(lambda x: str(x.isocalendar()[0]) + "/" + str(x.isocalendar()[1]))
    weekdaypair['date'] = weekdays['date'].apply(lambda x: str(x.isocalendar()[0]) + "/" + str(x.isocalendar()[1]))

    weekendpair = weekendpair.groupby('date').mean().reset_index()
    weekdaypair = weekdaypair.groupby('date').mean().reset_index()

    weeklyWeekend = (stats.normaltest(weekendpair['comment_count']))[1]
    weeklyWeekday = (stats.normaltest(weekdaypair['comment_count']))[1]
    weeklyLevene = (stats.levene(weekdaypair['comment_count'], weekendpair['comment_count']))[1]

    weeklyTtest = (stats.ttest_ind(weekendpair['comment_count'], weekdaypair['comment_count']))[1]

    uTest = (stats.mannwhitneyu(weekdays['comment_count'], weekends['comment_count']))[1]


    print(OUTPUT_TEMPLATE.format(
        initial_ttest_p=initialt,
        initial_weekday_normality_p=initialweekday,
        initial_weekend_normality_p=initialweekend,
        initial_levene_p=initialLevene,
        transformed_weekday_normality_p=transformweekday,
        transformed_weekend_normality_p=transformweekend,
        transformed_levene_p=transformLevene,
        weekly_weekday_normality_p=weeklyWeekday,
        weekly_weekend_normality_p=weeklyWeekend,
        weekly_levene_p=weeklyLevene,
        weekly_ttest_p=weeklyTtest,
        utest_p=uTest,
    ))


if __name__ == '__main__':
    main()