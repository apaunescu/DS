import numpy as np
import pandas as pd
import scipy.stats as stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

data = pd.read_csv('data.csv')

#['qs1', 'qs2', 'qs3', 'qs4', 'qs5', 'merge1', 'partition_sort']

qs1 = data[(data['algorithm'] == 'qs1')]
qs2 = data[(data['algorithm'] == 'qs2')]
qs3 = data[(data['algorithm'] == 'qs3')]
qs4 = data[(data['algorithm'] == 'qs4')]
qs5 = data[(data['algorithm'] == 'qs5')]
merge1 = data[(data['algorithm'] == 'merge1')]
partition_sort = data[(data['algorithm'] == 'partition_sort')]

qs1 = qs1.reset_index(drop=True)
qs2 = qs2.reset_index(drop=True)
qs3 = qs3.reset_index(drop=True)
qs4 = qs4.reset_index(drop=True)
qs5 = qs5.reset_index(drop=True)
merge1 = merge1.reset_index(drop=True)
partition_sort = partition_sort.reset_index(drop=True)

print(qs1)

anova = stats.f_oneway(qs1['total_time'], qs2['total_time'], qs3['total_time'], qs4['total_time'], qs5['total_time'], merge1['total_time'], partition_sort['total_time'])


print(qs1['total_time'].mean(), qs2['total_time'].mean(), qs3['total_time'].mean() ,qs4['total_time'].mean(), qs5['total_time'].mean(), merge1['total_time'].mean(), partition_sort['total_time'].mean())
x_data = pd.DataFrame({'qs1':qs1['total_time'], 'qs2':qs2['total_time'], 'qs3':qs3['total_time'], 'qs4':qs4['total_time'], 'qs5':qs5['total_time'], 'merg1':merge1['total_time'], 'partition_sort':partition_sort['total_time']})
x_melt = pd.melt(x_data)
print(x_data)

posthoc = pairwise_tukeyhsd(
	x_melt['value'], x_melt['variable'],
	alpha = 0.05)

#anova1 = stats.f_oneway(qs1['total_time'], qs2['total_time'])
print(posthoc)