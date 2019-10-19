#import the libraries
import matplotlib.pyplot as plt
import numpy as np # linear algebra
import pandas as pd
import pickle
import seaborn as sns
import sklearn
from sklearn.model_selection import cross_val_predict
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
import warnings
from sklearn.exceptions import DataConversionWarning
warnings.filterwarnings(action='ignore')
from sklearn import preprocessing
from sklearn.svm import SVC
from sklearn import tree
from sklearn.model_selection import cross_validate
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn.model_selection import cross_validate
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import f1_score

df = pd.read_csv('/Users/shiksharawat/Desktop/updateddata2.csv')
df.drop(columns= 'Unnamed: 0',inplace = True)
#taking data around mean for latitude and longitude
p = df['LOCATION_LONGITUDE'].mean()
lower = p - 0.02
upper = p + 0.02
df = df[df['LOCATION_LONGITUDE']>=lower]
df = df[df['LOCATION_LONGITUDE']<=upper]
​
q = df['LOCATION_LATITUDE'].mean()
lowerl = q - 0.07
upperl = q + 0.07
df = df[df['LOCATION_LATITUDE']>=lowerl]
df = df[df['LOCATION_LATITUDE']<=upperl]

df = df[df['Year']>=2016]
df = df[df['Year']<=2019]
df = df[df['Hour']>=0]
df = df[df['Hour']<=23]
df = df[df['Month']>=0]
df = df[df['Month']<=11]

#normalization
cols_to_norm = ['Hour','Date','Month','Year','LOCATION_LONGITUDE','LOCATION_LATITUDE']
df[cols_to_norm] = df[cols_to_norm].apply(lambda x: (x - x.min()))

def dist(pickup_longitude,pickup_latitude,dropoff_longitude,dropoff_latitude):
    pickup_longitude,pickup_latitude,dropoff_longitude,dropoff_latitude = map(np.radians, [pickup_longitude,pickup_latitude,dropoff_longitude,dropoff_latitude])
    dlon = dropoff_longitude - pickup_longitude
    dlat = dropoff_latitude - pickup_latitude
    a = np.sin(dlat/2.0)**2 + np.cos(pickup_latitude) * np.cos(dropoff_latitude) * np.sin(dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    distance = 6367 * c
    return distance

x = [[0,0,0,2019,85.438446,23.410040]]
distance = 100000000
for i in range(0,4000):
    t = [np.array(df.iloc[i,:])]
    distance = min(distance, dist(t[0][4],x[0][5],x[0][4],x[0][5]))
x[0].append(distance)


latitude = [23.5735,23.642,23.6470,23.6629,23.3600,23.4345,22.3615,23.4413,23.4840,23.4420,23.3047,23.4052,23.7510,23.4207,
            23.3987,23.1960,23.1793,23.2448,23.3298,23.2065,23.4190]
longitude = [84.9349,85.3362,85,3214,86.1014,85.4277,85.4791,85.4737,85.2124,85.4852,85.5844,85.4556,85.4672,85.7077,85.7487,85.7487,85.7538,85.3766,85.2438,85.2209]
r_b = [0,1,1,1,1,0,0,1,0,0,1,1,0,0,1,1,1]
r = 0
for i in range(0,20):
    dis = dist(x[0][4],x[0][5],latitude[i],longitude[i])
    if(dis<distance):
        distance = dis
        r = r_b[i]
x[0].append(r)


a = []


#theft
weights = np.linspace(0.05, 0.95, 20)
weight1 = []
f1score1 = []
copy = df.copy()
replace_map = {'Crime' : {'Attempt to Murder' : 0, 'Harassment' : 0 , 'Rape' : 0, 'Theft' : 1}}
copy.replace(replace_map, inplace = True)
target  = copy['Crime']
#new_copy = df.copy()
#new_copy.drop(columns = 'CRIME' , inplace = True)
X_train, X_test, y_train, y_test= train_test_split(df.drop(columns = 'Crime'), target , random_state=111)
from sklearn.linear_model import LogisticRegression
for i in weights:
    lr = LogisticRegression(random_state = 1, class_weight = {0: i, 1: 1.0-i})
    lr.fit(X_train,y_train)
    pred = lr.predict(X_test)
    weight1.append(i)
    f1score1.append(f1_score(y_test,pred))
index1 = 0
score1 = 0
for i in range(len(f1score1)):
    if(f1score1[i]>score1):
        score1 = f1score1[i]
        index1 = i
weight_ans1  = weight1[index1]

#DecisionTreeClassifier
#theft
weight2 = []
f1score2 = []
copy = df.copy()
replace_map = {'Crime' : {'Attempt to Murder' : 0, 'Harassment' : 0 , 'Rape' : 0, 'Theft' : 1}}
copy.replace(replace_map, inplace = True)
target  = copy['Crime']
#new_copy = df.copy()
#new_copy.drop(columns = 'CRIME' , inplace = True)
X_train, X_test, y_train, y_test= train_test_split(df.drop(columns = 'Crime'), target , random_state=111)
for i in weights:
    decision_tree = DecisionTreeClassifier(random_state= 111, max_depth=i , class_weight = {0: i, 1: 1.0-i})
    decision_tree.fit(X_train, y_train)
    pred = decision_tree.predict(X_test)
    weight2.append(i)
    f1score2.append(f1_score(y_test,pred))

index2 = 0
score2 = 0
for i in range(len(f1score2)):
    if(f1score2[i]>score2):
        score2 = f1score2[i]
        index2 = i
weight_ans2  = weight2[index2]

height = []
f1score3 = []
from sklearn import tree
from sklearn.model_selection import cross_validate
from sklearn.tree import DecisionTreeClassifier
#for theft
copy = df.copy()
replace_map = {'Crime' : {'Attempt to Murder' : 0, 'Harassment' : 0, 'Rape' : 0, 'Theft' : 1}}
copy.replace(replace_map, inplace = True)
target  = copy['Crime']
X_train, X_test, y_train, y_test= train_test_split(df.drop(columns = 'Crime'), target , random_state=111)
for i in range(1,10):
    decision_tree = DecisionTreeClassifier(random_state= 111, max_depth=i , class_weight = {0:weight_ans2, 1 : 1 -weight_ans2})
    decision_tree.fit(X_train, y_train)
    pred = decision_tree.predict(X_test)
    height.append(i)
    f1score3.append(f1_score(y_test,pred))

index = 0
score4 = 0
for i in range(len(f1score3)):
    if(f1score3[i]>score4):
        score4 = f1score3[i]
        index = i
height_ans  = height[index]



if(score1>score4):
    copy = df.copy()
    replace_map = {'Crime' : {'Attempt to Murder' : 0, 'Harassment' : 0 , 'Rape' : 0, 'Theft' : 1}}
    copy.replace(replace_map, inplace = True)
    target  = copy['Crime']
    lr = LogisticRegression(random_state = 1, class_weight = {0: weight_ans1, 1: 1-weight_ans1})
    lr.fit(df.drop(columns = 'Crime') , target)
    p = lr.predict_proba(x)[:,1]
    a.append(p[0])
else:
    copy = df.copy()
    replace_map = {'Crime' : {'Attempt to Murder' : 0, 'Harassment' : 0 , 'Rape' : 0, 'Theft' : 1}}
    copy.replace(replace_map, inplace = True)
    target  = copy['Crime']
    decision_tree = DecisionTreeClassifier(max_depth= height_ans, class_weight = {0:weight_ans2, 1 : 1-weight_ans2})
    decision_tree.fit(df.drop(columns = 'Crime') , target)
    pt = decision_tree.predict_proba(x)[:,1]
    a.append(pt[0])







#rape
weights = np.linspace(0.05, 0.95, 20)
weight1 = []
f1score1 = []
copy = df.copy()
replace_map = {'Crime' : {'Attempt to Murder' : 0, 'Harassment' : 0 , 'Rape' : 1, 'Theft' : 0}}
copy.replace(replace_map, inplace = True)
target  = copy['Crime']
#new_copy = df.copy()
#new_copy.drop(columns = 'CRIME' , inplace = True)
X_train, X_test, y_train, y_test= train_test_split(df.drop(columns = 'Crime'), target , random_state=111)
from sklearn.linear_model import LogisticRegression
for i in weights:
    lr = LogisticRegression(random_state = 1, class_weight = {0: i, 1: 1.0-i})
    lr.fit(X_train,y_train)
    pred = lr.predict(X_test)
    weight1.append(i)
    f1score1.append(f1_score(y_test,pred))
index1 = 0
score1 = 0
for i in range(len(f1score1)):
    if(f1score1[i]>score1):
        score1 = f1score1[i]
        index1 = i
weight_ans1  = weight1[index1]

#DecisionTreeClassifier

weight2 = []
f1score2 = []
copy = df.copy()
replace_map = {'Crime' : {'Attempt to Murder' : 0, 'Harassment' : 0 , 'Rape' : 1, 'Theft' : 0}}
copy.replace(replace_map, inplace = True)
target  = copy['Crime']
#new_copy = df.copy()
#new_copy.drop(columns = 'CRIME' , inplace = True)
X_train, X_test, y_train, y_test= train_test_split(df.drop(columns = 'Crime'), target , random_state=111)
for i in weights:
    decision_tree = DecisionTreeClassifier(random_state= 111, max_depth=i , class_weight = {0: i, 1: 1.0-i})
    decision_tree.fit(X_train, y_train)
    pred = decision_tree.predict(X_test)
    weight2.append(i)
    f1score2.append(f1_score(y_test,pred))

index2 = 0
score2 = 0
for i in range(len(f1score2)):
    if(f1score2[i]>score2):
        score2 = f1score2[i]
        index2 = i
weight_ans2  = weight2[index2]

height = []
f1score3 = []
from sklearn import tree
from sklearn.model_selection import cross_validate
from sklearn.tree import DecisionTreeClassifier
#for theft
copy = df.copy()
replace_map = {'Crime' : {'Attempt to Murder' : 0, 'Harassment' : 0, 'Rape' : 0, 'Theft' : 1}}
copy.replace(replace_map, inplace = True)
target  = copy['Crime']
X_train, X_test, y_train, y_test= train_test_split(df.drop(columns = 'Crime'), target , random_state=111)
for i in range(1,10):
    decision_tree = DecisionTreeClassifier(random_state= 111, max_depth=i , class_weight = {0:weight_ans2, 1 : 1 -weight_ans2})
    decision_tree.fit(X_train, y_train)
    pred = decision_tree.predict(X_test)
    height.append(i)
    f1score3.append(f1_score(y_test,pred))

index = 0
score4 = 0
for i in range(len(f1score3)):
    if(f1score3[i]>score4):
        score4 = f1score3[i]
        index = i
height_ans  = height[index]

if(score1>score4):
    copy = df.copy()
    replace_map = {'Crime' : {'Attempt to Murder' : 0, 'Harassment' : 0 , 'Rape' : 0, 'Theft' : 1}}
    copy.replace(replace_map, inplace = True)
    target  = copy['Crime']
    lr = LogisticRegression(random_state = 1, class_weight = {0: weight_ans1, 1: 1-weight_ans1})
    lr.fit(df.drop(columns = 'Crime') , target)
    p = lr.predict_proba(x)[:,1]
    a.append(p[0])
else:
    copy = df.copy()
    replace_map = {'Crime' : {'Attempt to Murder' : 0, 'Harassment' : 0 , 'Rape' : 0, 'Theft' : 1}}
    copy.replace(replace_map, inplace = True)
    target  = copy['Crime']
    decision_tree = DecisionTreeClassifier(max_depth= height_ans, class_weight = {0:weight_ans2, 1 : 1-weight_ans2})
    decision_tree.fit(df.drop(columns = 'Crime') , target)
    pt = decision_tree.predict_proba(x)[:,1]
    a.append(pt[0])

#harassment
weights = np.linspace(0.05, 0.95, 20)
weight1 = []
f1score1 = []
copy = df.copy()
replace_map = {'Crime' : {'Attempt to Murder' : 0, 'Harassment' : 1 , 'Rape' : 0, 'Theft' : 0}}
copy.replace(replace_map, inplace = True)
target  = copy['Crime']
#new_copy = df.copy()
#new_copy.drop(columns = 'CRIME' , inplace = True)
X_train, X_test, y_train, y_test= train_test_split(df.drop(columns = 'Crime'), target , random_state=111)
from sklearn.linear_model import LogisticRegression
for i in weights:
    lr = LogisticRegression(random_state = 1, class_weight = {0: i, 1: 1.0-i})
    lr.fit(X_train,y_train)
    pred = lr.predict(X_test)
    weight1.append(i)
    f1score1.append(f1_score(y_test,pred))
index1 = 0
score1 = 0
for i in range(len(f1score1)):
    if(f1score1[i]>score1):
        score1 = f1score1[i]
        index1 = i
weight_ans1  = weight1[index1]

#DecisionTreeClassifier
#theft
weight2 = []
f1score2 = []
copy = df.copy()
replace_map = {'Crime' : {'Attempt to Murder' : 0, 'Harassment' : 1, 'Rape' : 0, 'Theft' : 0}}
copy.replace(replace_map, inplace = True)
target  = copy['Crime']
#new_copy = df.copy()
#new_copy.drop(columns = 'CRIME' , inplace = True)
X_train, X_test, y_train, y_test= train_test_split(df.drop(columns = 'Crime'), target , random_state=111)
for i in weights:
    decision_tree = DecisionTreeClassifier(random_state= 111, max_depth=i , class_weight = {0: i, 1: 1.0-i})
    decision_tree.fit(X_train, y_train)
    pred = decision_tree.predict(X_test)
    weight2.append(i)
    f1score2.append(f1_score(y_test,pred))

index2 = 0
score2 = 0
for i in range(len(f1score2)):
    if(f1score2[i]>score2):
        score2 = f1score2[i]
        index2 = i
weight_ans2  = weight2[index2]

height = []
f1score3 = []
from sklearn import tree
from sklearn.model_selection import cross_validate
from sklearn.tree import DecisionTreeClassifier
#for theft
copy = df.copy()
replace_map = {'Crime' : {'Attempt to Murder' : 0, 'Harassment' : 0, 'Rape' : 0, 'Theft' : 1}}
copy.replace(replace_map, inplace = True)
target  = copy['Crime']
X_train, X_test, y_train, y_test= train_test_split(df.drop(columns = 'Crime'), target , random_state=111)
for i in range(1,10):
    decision_tree = DecisionTreeClassifier(random_state= 111, max_depth=i , class_weight = {0:weight_ans2, 1 : 1 -weight_ans2})
    decision_tree.fit(X_train, y_train)
    pred = decision_tree.predict(X_test)
    height.append(i)
    f1score3.append(f1_score(y_test,pred))

index = 0
score4 = 0
for i in range(len(f1score3)):
    if(f1score3[i]>score4):
        score4 = f1score3[i]
        index = i
height_ans  = height[index]

if(score1>score4):
    copy = df.copy()
    replace_map = {'Crime' : {'Attempt to Murder' : 0, 'Harassment' : 0 , 'Rape' : 0, 'Theft' : 1}}
    copy.replace(replace_map, inplace = True)
    target  = copy['Crime']
    lr = LogisticRegression(random_state = 1, class_weight = {0: weight_ans1, 1: 1-weight_ans1})
    lr.fit(df.drop(columns = 'Crime') , target)
    p = lr.predict_proba(x)[:,1]
    a.append(p[0])
else:
    copy = df.copy()
    replace_map = {'Crime' : {'Attempt to Murder' : 0, 'Harassment' : 0 , 'Rape' : 0, 'Theft' : 1}}
    copy.replace(replace_map, inplace = True)
    target  = copy['Crime']
    decision_tree = DecisionTreeClassifier(max_depth= height_ans, class_weight = {0:weight_ans2, 1 : 1-weight_ans2})
    decision_tree.fit(df.drop(columns = 'Crime') , target)
    pt = decision_tree.predict_proba(x)[:,1]
    a.append(pt[0])

#murder
weights = np.linspace(0.05, 0.95, 20)
weight1 = []
f1score1 = []
copy = df.copy()
replace_map = {'Crime' : {'Attempt to Murder' : 1, 'Harassment' : 0, 'Rape' : 0, 'Theft' : 0}}
copy.replace(replace_map, inplace = True)
target  = copy['Crime']
#new_copy = df.copy()
#new_copy.drop(columns = 'CRIME' , inplace = True)
X_train, X_test, y_train, y_test= train_test_split(df.drop(columns = 'Crime'), target , random_state=111)
from sklearn.linear_model import LogisticRegression
for i in weights:
    lr = LogisticRegression(random_state = 1, class_weight = {0: i, 1: 1.0-i})
    lr.fit(X_train,y_train)
    pred = lr.predict(X_test)
    weight1.append(i)
    f1score1.append(f1_score(y_test,pred))
index1 = 0
score1 = 0
for i in range(len(f1score1)):
    if(f1score1[i]>score1):
        score1 = f1score1[i]
        index1 = i
weight_ans1  = weight1[index1]

#DecisionTreeClassifier
#theft
weight2 = []
f1score2 = []
copy = df.copy()
replace_map = {'Crime' : {'Attempt to Murder' : 1, 'Harassment' : 0, 'Rape' : 0, 'Theft' : 0}}
copy.replace(replace_map, inplace = True)
target  = copy['Crime']
#new_copy = df.copy()
#new_copy.drop(columns = 'CRIME' , inplace = True)
X_train, X_test, y_train, y_test= train_test_split(df.drop(columns = 'Crime'), target , random_state=111)
for i in weights:
    decision_tree = DecisionTreeClassifier(random_state= 111, max_depth=i , class_weight = {0: i, 1: 1.0-i})
    decision_tree.fit(X_train, y_train)
    pred = decision_tree.predict(X_test)
    weight2.append(i)
    f1score2.append(f1_score(y_test,pred))

index2 = 0
score2 = 0
for i in range(len(f1score2)):
    if(f1score2[i]>score2):
        score2 = f1score2[i]
        index2 = i
weight_ans2  = weight2[index2]

height = []
f1score3 = []
from sklearn import tree
from sklearn.model_selection import cross_validate
from sklearn.tree import DecisionTreeClassifier
#for theft
copy = df.copy()
replace_map = {'Crime' : {'Attempt to Murder' : 0, 'Harassment' : 0, 'Rape' : 0, 'Theft' : 1}}
copy.replace(replace_map, inplace = True)
target  = copy['Crime']
X_train, X_test, y_train, y_test= train_test_split(df.drop(columns = 'Crime'), target , random_state=111)
for i in range(1,10):
    decision_tree = DecisionTreeClassifier(random_state= 111, max_depth=i , class_weight = {0:weight_ans2, 1 : 1 -weight_ans2})
    decision_tree.fit(X_train, y_train)
    pred = decision_tree.predict(X_test)
    height.append(i)
    f1score3.append(f1_score(y_test,pred))

index = 0
score4 = 0
for i in range(len(f1score3)):
    if(f1score3[i]>score4):
        score4 = f1score3[i]
        index = i
height_ans  = height[index]

if(score1>score4):
    copy = df.copy()
    replace_map = {'Crime' : {'Attempt to Murder' : 0, 'Harassment' : 0 , 'Rape' : 0, 'Theft' : 1}}
    copy.replace(replace_map, inplace = True)
    target  = copy['Crime']
    lr = LogisticRegression(random_state = 1, class_weight = {0: weight_ans1, 1: 1-weight_ans1})
    lr.fit(df.drop(columns = 'Crime') , target)
    p = lr.predict_proba(x)[:,1]
    a.append(p[0])
else:
    copy = df.copy()
    replace_map = {'Crime' : {'Attempt to Murder' : 0, 'Harassment' : 0 , 'Rape' : 0, 'Theft' : 1}}
    copy.replace(replace_map, inplace = True)
    target  = copy['Crime']
    decision_tree = DecisionTreeClassifier(max_depth= height_ans, class_weight = {0:weight_ans2, 1 : 1-weight_ans2})
    decision_tree.fit(df.drop(columns = 'Crime') , target)
    pt = decision_tree.predict_proba(x)[:,1]
    a.append(pt[0])

import math
np.array(a)
class_weights = [0.1, 0.3, 0.2, 0.4]
np.array(class_weights)
p = np.multiply(a,class_weights)
ans = 1/(1+ math.exp(-1*(sum(p))))


safety = []
df = pd.read_csv('/Users/shiksharawat/Desktop/updateddata2.csv')
df.drop(columns= 'Unnamed: 0',inplace = True)
new_df = df.copy()
new_df.drop(columns = 'Crime',inplace = True)


for i in range(0,300):
    #murder
    abc = []
    x = [np.array(new_df.iloc[i,:])]
    df = pd.read_csv('/Users/shiksharawat/Desktop/updateddata2.csv')
    df.drop(columns= 'Unnamed: 0',inplace = True)
    copy = df.copy()
    replace_map = {'Crime' : {'Attempt to Murder' : 1, 'Harassment' : 0 , 'Rape' : 0, 'Theft' : 0}}
    copy.replace(replace_map, inplace = True)
    target  = copy['Crime']
    lr = LogisticRegression(class_weight = {0: 0.05, 1: 0.95})
    lr.fit(df.drop(columns = 'Crime'),target)
    p = lr.predict_proba(x)[:,1]
    abc.append(p[0])



    #harassment
    copy = df.copy()
    df = pd.read_csv('/Users/shiksharawat/Desktop/updateddata2.csv')
    df.drop(columns= 'Unnamed: 0',inplace = True)
    replace_map = {'Crime' : {'Attempt to Murder' : 0, 'Harassment' : 1 , 'Rape' : 0, 'Theft' : 0}}
    copy.replace(replace_map, inplace = True)
    target  = copy['Crime']
    lr = LogisticRegression(class_weight = {0: 0.05, 1: 0.95})
    lr.fit(df.drop(columns = 'Crime'),target)
    p = lr.predict_proba(x)[:,1]
    abc.append(p[0])


    #rape
    copy = df.copy()
    df = pd.read_csv('/Users/shiksharawat/Desktop/updateddata2.csv')
    df.drop(columns= 'Unnamed: 0',inplace = True)
    replace_map = {'Crime' : {'Attempt to Murder' : 0, 'Harassment' : 0 , 'Rape' : 1, 'Theft' : 0}}
    copy.replace(replace_map, inplace = True)
    target  = copy['Crime']
    lr = LogisticRegression(class_weight = {0: 0.05, 1: 0.95})
    lr.fit(df.drop(columns = 'Crime'),target)
    p = lr.predict_proba(x)[:,1]
    abc.append(p[0])

    #theft
    copy = df.copy()
    df = pd.read_csv('/Users/shiksharawat/Desktop/updateddata2.csv')
    df.drop(columns= 'Unnamed: 0',inplace = True)
    replace_map = {'Crime' : {'Attempt to Murder' : 0, 'Harassment' : 0 , 'Rape' : 0, 'Theft' : 1}}
    copy.replace(replace_map, inplace = True)
    target  = copy['Crime']
    lr = LogisticRegression(class_weight = {0: 0.05, 1: 0.95})
    lr.fit(df.drop(columns = 'Crime'),target)
    p = lr.predict_proba(x)[:,1]
    abc.append(p[0])


    import math
    np.array(a)
    class_weights = [0.4, 0.2, 0.3, 0.1]
    np.array(class_weights)
    p = np.multiply(abc,class_weights)
    ans = 1/(1+ math.exp(-1*(sum(p))))
    safety.append(ans)


safety_index = max(safety)
