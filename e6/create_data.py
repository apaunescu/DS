import time
from implementations import all_implementations
import numpy as np
import pandas as pd

random_array = np.random.rand(25000)
print(random_array)

#data = pd.DataFrame(columns = ['starting_time', 'end_time', 'algorithm'])
#Learned how to append data here - https://stackoverflow.com/questions/31674557/how-to-append-rows-in-a-pandas-dataframe-in-a-for-loop/42723801
cols = ['starting_time', 'end_time', 'total_time', 'algorithm']
lst = []
algorithm = ['qs1', 'qs2', 'qs3', 'qs4', 'qs5', 'merge1', 'partition_sort']
index = 0

for i in range (0, 40):
	for sort in all_implementations:
		st = time.time()
		res = sort(random_array)
		en = time.time()
		total_time = (en - st)
		lst.append([st, en, total_time, algorithm[index % 7]])
		index += 1
	    #data['starting_time'] = data['starting_time'].append(st)
	    #data['end_time'] = data['end_time'].append(en)
	    #data['algorithm'] = data['algorithm'].append(res)


data = pd.DataFrame(lst, columns = cols)
data.to_csv('data.csv', index=False)