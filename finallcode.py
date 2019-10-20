#import the libraries
import sys
import matplotlib.pyplot as plt
import numpy as np # linear algebra
import pandas as pd

import sklearn
from sklearn.model_selection import train_test_split


from sklearn import preprocessing
from sklearn.svm import SVC
from sklearn import tree

from sklearn.tree import DecisionTreeClassifier
print("check")
df = pd.read_csv('./public/hack2.csv')
print("morning")
hour =int(sys.argv[1])
date = int(sys.argv[2])
month = int(sys.argv[3])
year = int(sys.argv[4])
longitude = float(sys.argv[5])
latitude = float(sys.argv[6])
print(hour)

x = [[hour,date,month,year,longitude,latitude]]
a = []

#murder
copy = df.copy()
replace_map = {'CRIME' : {'Attempt to Murder' : 1, 'Harassment' : 0 , 'Rape' : 0, 'Theft' : 0}}
copy.replace(replace_map, inplace = True)
target  = copy['CRIME']
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression(random_state = 1, class_weight = {0: 0.07, 1: 0.93})
lr.fit(df.drop(columns = 'CRIME') , target)
p = lr.predict_proba(x)[:,1]
a.append(p[0])



#harassment
copy = df.copy()
replace_map = {'CRIME' : {'Attempt to Murder' : 0, 'Harassment' : 1 , 'Rape' : 0, 'Theft' : 0}}
copy.replace(replace_map, inplace = True)
target  = copy['CRIME']
clf = SVC(gamma= 2,class_weight = {0: 0.05, 1: 0.95}, probability = True)
clf.fit(df.drop(columns = 'CRIME') , target)
p = clf.predict_proba(x)[:,1]
a.append(p[0])


#rape
copy = df.copy()
replace_map = {'CRIME' : {'Attempt to Murder' : 0, 'Harassment' : 0 , 'Rape' : 1, 'Theft' : 0}}
copy.replace(replace_map, inplace = True)
target  = copy['CRIME']
decision_tree = DecisionTreeClassifier(max_depth= 6, class_weight = {0:.4, 1 : 0.6})
decision_tree.fit(df.drop(columns = 'CRIME') , target)
p = decision_tree.predict_proba(x)[:,1]
a.append(p[0])


#theft
copy = df.copy()
replace_map = {'CRIME' : {'Attempt to Murder' : 0, 'Harassment' : 0 , 'Rape' : 1, 'Theft' : 0}}
copy.replace(replace_map, inplace = True)
target  = copy['CRIME']
clr = SVC(gamma= 2,class_weight = {0: 0.05, 1: 0.95}, probability = True)
clr.fit(df.drop(columns = 'CRIME') , target)
p = clr.predict_proba(x)[:,1]
a.append(p[0])
print(a)

import math
np.array(a)
class_weights = [0.4, 0.2, 0.3, 0.1]
np.array(class_weights)
p = np.multiply(a,class_weights)
ans = 1/(1+ math.exp(-1*(sum(p))))
print(ans)

#0.6317589799363152