import pandas as pd
import numpy as np
import difflib
import sys


textFile = sys.argv[1]
csvFile = sys.argv[2]
output = sys.argv[3]

def cleaner(string):
	string = string.rstrip('\n')
	return string

def realTitle(title):
	match = difflib.get_close_matches(title, movies['title'], n=100, cutoff=0.6)
	if (match == []):
		match = "Z"
	return match[0]


movieLegend = open(textFile, "r")
titles = movieLegend.readlines()
movies = pd.DataFrame(data = titles,
	columns = ['title'])
movies['title'] = movies['title'].apply(cleaner)
userRatings = pd.read_csv(csvFile)


userRatings['title'] = userRatings['title'].apply(realTitle)
userRatings = userRatings.groupby('title').mean().reset_index()
userRatings.rating = userRatings.rating.round(2)
userRatings = userRatings[userRatings['title'] != "Z"]

userRatings.to_csv(output)
#print(userRatings)


