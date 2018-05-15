import numpy as np
import matplotlib.pyplot as plt

data = np.load('monthdata.npz')
totals = data['totals']
counts = data['counts']

sumOfRows = np.sum(totals, axis = 1)
print(sumOfRows)
lowest = np.argmin(sumOfRows)
print("Row with the lowest total precipitation: \n", lowest)

totalPrecip = np.sum(totals, axis = 0)
countsPrecip = np.sum(counts, axis = 0)
print("Average precipitation in each month: \n", totalPrecip / countsPrecip)

totalPrecip2 = np.sum(totals, axis = 1)
countsPrecip2 = np.sum(counts, axis = 1)
print("Average precipitation in each city: \n", totalPrecip2 / countsPrecip2)

height = 4 * totals.shape[0]
totals = np.reshape(totals,(height, 3))
newSum = np.sum(totals, axis = 1)
newSum = np.reshape(newSum,(height // 4, 4))
print("Quarterly precipitation totals: \n", newSum)








