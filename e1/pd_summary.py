import pandas as pd

totals = pd.read_csv('totals.csv').set_index(keys=['name'])
counts = pd.read_csv('counts.csv').set_index(keys=['name'])

df = totals.sum(axis = 1)
lowest = pd.Series.idxmin(df)
print("City with the lowest total precipitation:\n", lowest)

df = totals.sum(axis = 0)
df1 = counts.sum(axis = 0)
print("Average precipitation in each month:\n", df / df1)

totalPrecip2 = totals.sum(axis = 1)
countsPrecip2 = counts.sum(axis = 1)
print("Average precipitation in each city:\n", totalPrecip2 / countsPrecip2)
