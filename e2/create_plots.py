import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys

filename1 = sys.argv[1]
filename2 = sys.argv[2]

first = pd.read_table(filename1, sep=' ', header=None, index_col=1,
        names=['lang', 'page', 'views', 'bytes'])

second = pd.read_table(filename2, sep=' ', header=None, index_col=1,
        names=['lang', 'page', 'views', 'bytes'])


first = first.sort_values(by = 'views', ascending = False)

views = first['views'].values
print(views)

third = first.merge(second, how ='inner', left_index = True, right_index = True)
viewsx = third.views_x
viewsy = third.views_y

plt.figure(figsize=(10, 5)) # change the size to something sensible
plt.subplot(1, 2, 1) # subplots in 1 row, 2 columns, select the first
plt.plot(views) # build plot 1
plt.subplot(1, 2, 2) # ... and then select the second
plt.xscale('log', viewsx)
plt.yscale('log', viewsy)
plt.scatter(viewsx, viewsy) # build plot 2
plt.show()