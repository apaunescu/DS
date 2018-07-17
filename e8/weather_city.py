import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier


labelled = pd.read_csv(sys.argv[1])
unlabelled = pd.read_csv(sys.argv[2])


data = labelled.as_matrix(columns = labelled.columns[2:])
data = StandardScaler().fit_transform(data)

unlabeled_data = unlabelled.as_matrix(columns = unlabelled.columns[2:])
unlabeled_data = StandardScaler().fit_transform(unlabeled_data)


X = data
y = labelled['city'].values
#print(y)

X_train, X_test, y_train, y_test = train_test_split(X, y)

clf = KNeighborsClassifier()
clf.fit(X_train,y_train)
y_predicted = clf.predict(unlabeled_data)
print(clf.score(X_test, y_test))	
predictions = y_predicted
#print(y_predicted)
output = pd.Series(predictions).to_csv(sys.argv[3], index=False)

#df = pd.DataFrame({'truth': y_test, 'prediction': clf.predict(X_test)})
#print(df[df['truth'] != df['prediction']])

#X_train, y_train = train[]
#X_test, y_test = test[X_columns], test[y_column]


#print(train)