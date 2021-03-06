# -*- coding: utf-8 -*-
"""HousePrice.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Mada0S-OUBAWZS3mCDQds1ewN3xbtwq-

# Importing the essential libraries
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

"""# Data Gathering"""

# The original dataframe is available on my drive at https://drive.google.com/file/d/1QOuRVokiUC6Q2JiB4TaMZDNnBKcq3qs8/view?usp=sharing
odf=pd.read_csv('/content/drive/MyDrive/IBM/DataAnalysis/kc_house_data.csv')

df=odf
df.head(20)

"""# Data wrangling

1- Checking for missing values
"""

df.isnull().sum()
#nice

""" 2- Check for outliers and noise data"""

pd.DataFrame(df.describe())

# Price column it seems to be normal because of the values of min and max are accepted

# For number of bedrooms
print(df['bedrooms'].value_counts())

df['bedrooms'].iloc[df[df['bedrooms']==33].index[0]]=10
df['bedrooms'].iloc[df[df['bedrooms']==11].index[0]]=10

# For number of bathrooms
print(df['bathrooms'].value_counts())
print("++++++++++++++++++++++")
lst=list(df['bathrooms'])
for i,v in enumerate(lst):
  lst[i]=int(v)
  if lst[i] == 0:
    lst[i]=1
  if ((v==7) or (v==8)):
    lst[i]=6

df['bathrooms']=lst
df['bathrooms'].value_counts()

# For sqft_living and	sqft_lot I will do nothing because I will do 
# the analysis useing the updated two columns sqft_living15 and sqft_lot15

# For number of floors

lst=df['floors']
for i,v in enumerate(lst):
  lst[i]=int(v)

df['floors']=lst
df['floors'].value_counts()

# For waterfront, view, condition, grade, sqft_above,	sqft_basement,	yr_built, 
# lat, and long, after test print them value_counts they seem to be normal !

# For yr_renovated column

print(df['yr_renovated'].min())
# I intend to show this, there is a 0 as minimum which is un logic 
#  but do not worry about it, in the next section which is feature extraction I will 
#  embedded yr_renovated and yr_built columns in one and handle it there.

# For latitude angle column 
print('The minimum angle is: {}'.format(df['lat'].min()))
print('The maximum angle is: {}'.format(df['lat'].max()))
#Those two values are almost the same to the actual value which is 47.5480?? N

# For longitude angle column 
print('The minimum angle is: {}'.format(df['long'].min()))
print('The maximum angle is: {}'.format(df['long'].max()))
#Those two values are almost the same to the actual value which is 121.9836?? W

# For sqft_living15 column the only thing I done is to remove the outliers

IQR=(2360.000000-1840.000000)
uo=2360.000000+(1.5*IQR) #Upper outlier
lo=1490.000000-(1.5*IQR) #Lower outlier

for i,v in enumerate(df['sqft_living15']):
  if v > uo :
    df['sqft_living15'].iloc[i] = uo
  if v < lo :
    df['sqft_living15'].iloc[i] = lo

# For sqft_lot15 column the only thing I done is to remove the outliers

IQR=(10083.000000-5100.000000)
uo=10083.000000+(1.5*IQR) #Upper outlier
lo=7620.000000 -(1.5*IQR) #Lower outlier

for i,v in enumerate(df['sqft_lot15']):
  if v > uo :
    df['sqft_lot15'].iloc[i] = uo
  if v < lo :
    df['sqft_lot15'].iloc[i] = lo

pd.DataFrame(df.describe())

"""3- Remove the duplicated rows"""

#The entire data must not contain any duplicated
print('The number of repeated rows for entire dataframe is {}'.format(df.duplicated().sum()))

# The only on column must not has any duplicated rows is the id, because it's a unique feature
print('The number of repeated rows for the ID column is {}'.format(df.duplicated(subset=['id']).sum()))
# Note: I will not drop this repeated rows because it maybe refares to the same unit sold many times between May2014 and May2015

# To ensure that I will drop the entire id column then search for any duplicate rows
test=df.drop(['id'],axis=1)

test.duplicated().sum()
#nice

"""3- Features Extraction"""

df.columns

# First I will extract the ages columns

age=[]

renewal_age=[]

drops=[]


for i,v in enumerate(df['yr_built']):
  r= df['yr_renovated'].iloc[i]

  age.append(2021-int(v))

  if (r <= v):
    renewal_age.append(0)
  else:
    renewal_age.append(2021-int(r))

# Then I will make the two datasets represents the inout and outout named x and y 

# For x: as mentioned earlier I will use the columns represent the specific features of units
#        I will use  ['bedrooms', 'bathrooms', 'floors', 'waterfront', 'view', 'condition', 'grade','sqft_living15', 'sqft_lot15']
#        till now, and in the next cell I will add the ages columns
x=pd.DataFrame(data = df , columns = ['bedrooms', 'bathrooms', 'floors', 
                                      'waterfront', 'view', 'condition', 'grade',
                                      'sqft_living15', 'sqft_lot15'])

floors=[int(x) for x in x['floors']]
x['floors']=floors

# For y: only the proce will be the output
y=pd.DataFrame(data=df , columns=['price'])



# Renamming the sqft_living15', 'sqft_lot15' columns and adding the ages columns

x.rename(columns={'sqft_living15':'sqft_living' , 'sqft_lot15':'sqft_lot'},inplace=True)
x['age']=age
x['renewal-age']=renewal_age
x.columns

x.describe()

drops=[]

for i,v in enumerate (x.duplicated()):
  if v == True:
    drops.append(i)

x.drop(drops,axis=0,inplace=True)

x.duplicated().sum()

y.drop(drops,axis=0,inplace=True)

print(len(y)==len(x))
# Ready to school !

"""#EDA

First for columns contain discrete values
"""

x.columns

fig=plt.figure()
ax=fig.add_axes([0,0,1,1])
o=0
for i in ['bedrooms', 'bathrooms', 'floors', 'waterfront', 'view', 'condition','grade']:
  ax=fig.add_axes([0,o,1,1])
  sb.countplot(data=x,x=i,ax=ax);
  plt.xlabel('{}'.format(str(i)).title());
  plt.legend();
  o+=1.5

fig=plt.figure()
ax=fig.add_axes([0,0,1,1])
o=0
for i in ['sqft_living', 'sqft_lot', 'age', 'renewal-age']:
  ax=fig.add_axes([0,o,1,1])
  ax.hist(data=x,x=i)
  plt.xlim((x[i].min(),x[i].max()))
  plt.xlabel('{}'.format(str(i)).title());
  plt.legend();
  o+=1.5

"""# Machine learning part  (For predicting the prices)"""

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression as LR
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import MinMaxScaler

x_train, x_test, y_train, y_test = train_test_split(x,y)

model=LR().fit(x_train,y_train)

y_pred_train=model.predict(x_train)
print('The Training R2 Score: {}'.format(r2_score(y_train,y_pred_train)))

y_pred_test=model.predict(x_test)
print('The Testing R2 Score: {}'.format(r2_score(y_test,y_pred_test)))

'''We can note that, the accuracy not enough high but there is not 
underfitting because the train and test metrices are almost the same. 
Just for trying I will do MinMaxScaler normalization to check if 
the high varaity of feature ranges causing this or not'''

from sklearn.preprocessing import MinMaxScaler

x_train, x_test, y_train, y_test = train_test_split(x,y)


scaler = MinMaxScaler().fit(x_train)
normalized_X = scaler.transform(x_train)
normalized_X_test = scaler.transform(x_test)


model_test=LR().fit(normalized_X,y_train)


y_pred_train=model_test.predict(normalized_X)
print('The Training R2 Score: {}'.format(r2_score(y_train,y_pred_train)))

y_pred_test=model_test.predict(normalized_X_test)
print('The Testing R2 Score: {}'.format(r2_score(y_test,y_pred_test)))

'''These accuracies measurements are almost the same to the model run 
without feature normalization so, it's recommended to use the first model'''