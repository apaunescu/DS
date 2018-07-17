import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys


textFile = sys.argv[1]
csvFile = sys.argv[2]


movieLegend = open(textFile, "r")
print ("name of my file: ", movieLegend.name)

userRatings = pd.read_csv(csvFile,
		names = ['title', 'rating'])


