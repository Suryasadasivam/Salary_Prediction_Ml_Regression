# -*- coding: utf-8 -*-
"""Salary_dataset_Analysis_Regressor .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fulsvuyN9Gtf8ABHOojJPM-dsz0BA662
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import statsmodels.api as sm
import plotly.express as px
from sklearn.preprocessing import OrdinalEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

from scipy import stats

df=pd.read_csv("/content/salaries.csv")

df.info()

df.describe()

df.head()

df.isnull().sum()

colum=df.columns

colum

for i in colum:
  print(df[i].unique())
  print("_________________")

new_job_title = {'Machine Learning Engineer' : 'ML Engineer',
                                           'Machine Learning Researcher': 'ML Engineer',
                                           'Machine Learning Research Engineer': 'ML Engineer',
                                           'MLOps Engineer' : 'ML Engineer',
                                           'ML Ops Engineer' : 'ML Engineer',
                                           'Lead Machine Learning Engineer' : 'ML Engineer',
                                           'Head of Machine Learning' : 'ML Engineer',
                                           'Machine Learning Operations Engineer' : 'ML Engineer',
                                           'Machine Learning Infrastructure Engineer' : 'ML Engineer',
                                           'Machine Learning Modeler' : 'ML Engineer',
                                           'Machine Learning Software Engineer' : 'ML Engineer',
                                           'Applied Machine Learning Scientist' : 'ML Engineer',
                                           'Machine Learning Manager' : 'ML Engineer',
                                           'Principal Machine Learning Engineer' : 'ML Engineer',
                                           'Staff Machine Learning Engineer' : 'ML Engineer',
                                           'Machine Learning Specialist' : 'ML Engineer',
                                           'Machine Learning Developer' : 'ML Engineer',
                                           'Applied Machine Learning Engineer' : 'ML Engineer',
                                           'Machine Learning Scientist' : 'ML Engineer',

                                           'Data Management Analyst' : 'Data Analyst',
                                           'Data Operations Analyst' : 'Data Analyst',
                                           'Data Quality Analyst' : 'Data Analyst',
                                           'Admin & Data Analyst' : 'Data Analyst',
                                           'Data Analyst Lead' : 'Data Analyst',
                                           'Lead Data Analyst' : 'Data Analyst',
                                           'Business Data Analyst' : 'Data Analyst',
                                           'Financial Data Analyst' : 'Data Analyst',
                                           'Staff Data Analyst' : 'Data Analyst',
                                           'Business Intelligence Data Analyst' : 'Data Analyst',
                                           'Finance Data Analyst' : 'Data Analyst',
                                           'Compliance Data Analyst' : 'Data Analyst',
                                           'Product Data Analyst' : 'Data Analyst',
                                           'Data Visualization Analyst' : 'Data Analyst',
                                           'Sales Data Analyst' : 'Data Analyst',
                                           'Marketing Data Analyst' : 'Data Analyst',
                                           'Principal Data Analyst' : 'Data Analyst',

                                           'Data Science Manager' : 'Data Science',
                                           'Data Science Consultant' : 'Data Science',
                                           'Data Science Director' : 'Data Science',
                                           'Data Science Engineer' : 'Data Science',
                                           'Data Science Practitioner' : 'Data Science',
                                           'Data Science Lead' : 'Data Science',
                                           'Director of Data Science' : 'Data Science',
                                           'Managing Director Data Science' : 'Data Science',
                                           'Head of Data Science' : 'Data Science',
                                           'Data Science Tech Lead' : 'Data Science',

                                           'Marketing Data Scientist' : 'Data Scientist',
                                           'Principal Data Scientist' : 'Data Scientist',
                                           'Applied Data Scientist' : 'Data Scientist',
                                           'Lead Data Scientist' : 'Data Scientist',
                                           'Staff Data Scientist' : 'Data Scientist',
                                           'Data Scientist Lead' : 'Data Scientist',

                                           'AI Architect' : 'AI Engineer',
                                           'AI Software Engineer' : 'AI Engineer',
                                           'AI Research Scientist' : 'AI Engineer',
                                           'AI Research Engineer' : 'AI Engineer',
                                           'AI Programmer' : 'AI Engineer',
                                           'AI Product Manager' : 'AI Engineer',
                                           'AI Developer' : 'AI Engineer',
                                           'AI Scientist' : 'AI Engineer'}

df['job_title'] = df['job_title'].replace(new_job_title)

df['job_title'].unique()

df['job_title'].value_counts()

continuous_columns = ['salary', 'salary_in_usd']
category_columns = ['work_year', 'experience_level', 'employment_type', 'job_title',
                    'salary_currency', 'employee_residence', 'remote_ratio', 'company_location', 'company_size']

def central_limit_theorem(continous_column,sample_size,rage):
  result_centrallimit={}
  pop=df[continous_column].values
  population_mean=pop.mean()
  allsample=[]
  for i in range(rage):
     sample=np.random.choice(pop,sample_size)
     allsample.append(sample.mean())
  all_sample_mean=(np.mean(allsample))
  result_centrallimit.update({'Column Name':continous_column,
                       'Population mean':population_mean,
                       'Allsample mean':all_sample_mean
                       })
  if continous_column:
    H0_accepted=0
    H0_rejected=0
    for i in range(rage):
      sample1=df[continous_column].sample(frac=0.04)
      t_test,p_value=stats.ttest_1samp(sample1,df[continous_column].mean())
      if p_value<0.05:
        H0_rejected+=1
      else:
        H0_accepted+=1
      if H0_accepted>H0_rejected:
        result_centrallimit.update({'Onesamplettest':' H0-There is no significant difference','Ttest':t_test,
                                    'pvalue':p_value})
      else:
        result_centrallimit.update({'Onesamplettest':' Ha-There is significant difference','Ttest':t_test,'pvalue':p_value})
    return(result_centrallimit)

res=[]
for i in continuous_columns:
  s=central_limit_theorem(i,50,10)
  res.append(s)
pd.DataFrame(res)

def twosamplettest(continous_column1,continous_column2,sample_size,rage):
   H0_accepted=0
   H0_rejected=0
   result={}
   allsample1=[]
   allsample2=[]
   for i in range(rage):
     sample1=df[continous_column1].sample(frac=0.2)
     sample2=df[continous_column2].sample(frac=0.2)
     t_test,p_value=stats.ttest_ind(sample1,sample2)
     if p_value<0.05:
        H0_rejected+=1
     else:
        H0_accepted+=1
     if H0_accepted>H0_rejected:
         result.update({
             'column':continous_column1+"&"+continous_column2,
             'twosamplettest':'H0-There is no significant difference',
             't_test_value':t_test,
              'P_value':p_value})
     else:
         result.update({
              'column':continous_column1+"&"+continous_column2,
             'twosamplettest':' Ha-There is significant difference',
              't_test_value':t_test,
              'P_value':p_value})
   if continous_column1:
     H0_accepted=0
     H0_rejected=0
     for i in range(rage):
         column1=df[continous_column1]
         column2=df[continous_column2]
         sample1=np.random.choice(column1,sample_size)
         sample2=np.random.choice(column2,sample_size)
         allsample1.append(sample1.mean())
         allsample2.append(sample2.mean())
     t_test,p_value=stats.ttest_ind(allsample1,allsample2)
     if p_value<0.05:
              H0_rejected+=1
     else:
            H0_accepted+=1
     if H0_accepted>H0_rejected:
              result.update({
             'column':continous_column1+"&"+continous_column2,
             'twosamplettest central':'H0-There is no significant difference',
             't_test_valuone':t_test,
             'P_valueone':p_value})
     else:
              result.update({
              'column':continous_column1+"&"+continous_column2,
             'twosamplettest central':' Ha-There is significant difference',
             't_test_valuone':t_test,
             'P_valueone':p_value})

   return result

columns=continuous_columns
res1=[]
for i in range (len(columns)-1):
  column1=columns[i]
  for j in range(i+1,len(columns)):
      column2=columns[j]
      j=twosamplettest(column1,column2,50,10)
      res1.append(j)
pd.DataFrame(res1)

def chi_square_test(category_column1,category_column2):
  result={}
  H0_accepted=0
  H0_rejected=0
  data1=pd.crosstab(df[category_column1],df[category_column2])
  observed_values=data1.values
  value=stats.chi2_contingency(observed_values)
  p_value=value[1]
  if p_value<0.05:
     H0_rejected+=1
  else:
    H0_accepted+=1
  if H0_accepted>H0_rejected:
    result.update({
        'column':category_column1+"&"+category_column2,
        "chi_square_test": "There is no relationship between two mentioned column" })
  else:
    result.update({
        'column':category_column1+"&"+category_column2,
        "chi_square_test": "There is relationship between two mentioned column" })

  return result

Category=category_columns
res2=[]
for i in range(len(Category)-1):
  category1=Category[i]
  for j in range(i+1,len(Category)):
      category2=Category[j]
      chi=chi_square_test(category1,category2)
      res2.append(chi)
pd.set_option('max_colwidth', None)
pd.DataFrame(res2)

def annova_test(continous_column,category_column):
   result={}
   H0_accepted=0
   H0_rejected=0
   group=df[category_column].unique()
   grp={}
   for i in group:
     grp[i]=df[continous_column][df[category_column]==i]
   f_value,p_value=stats.f_oneway(*grp.values())
   if p_value<0.05:
    H0_rejected+=1
   else:
     H0_accepted+=1
   if H0_accepted>H0_rejected:
     result.update({
        'column':continous_column+"&"+category_column,
        "Annova_test": "There is relationship between mentioned column"})
   else:
     result.update({
        'column':continous_column+"&"+category_column,
        "Annova_test": "There is no relationship between mentioned column"})

   return result

Category=category_columns
continous=continuous_columns
res3=[]
for i in continous:
  for j in Category:
    ann=annova_test(i,j)
    res3.append(ann)
pd.DataFrame(res3)

"""**Data Visualization**"""

fig = px.scatter(df, x="work_year", y="salary_in_usd")
fig.update_xaxes(tickvals=[2020,2021,2022, 2023, 2024])
fig.show()

sns.pairplot(df[['work_year', 'salary_in_usd', 'remote_ratio', 'company_size']])
plt.show()

fig = px.box (df,x="employment_type",y="salary_in_usd")
fig.show()

fig=px.sunburst(df,path=["work_year","experience_level","employment_type","remote_ratio","company_size"],values="salary_in_usd")
fig.show()

"""**Data Preprocessing**"""

columns=['experience_level', 'employment_type', 'job_title',
       'salary_currency', 'employee_residence',
       'company_location', 'company_size']

encode=OrdinalEncoder()
for i in columns:
  df[i]=encode.fit_transform(df[[i]])

df

x = df.drop(["salary", "salary_currency", "salary_in_usd"], axis = 1)
y = df["salary_in_usd"]

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.15)

model=RandomForestRegressor().fit(x_train,y_train)
y_pred=model.predict(x_test)

from sklearn.ensemble import AdaBoostRegressor
from sklearn.metrics import mean_squared_error

mse=mean_squared_error(y_test,y_pred)
mse

input = np.array([[2024, 2, 3, 24, 85, 50, 66, 0]])
prediction = model.predict(input)
prediction

model1=AdaBoostRegressor().fit(x_train,y_train)
y_pred1=model1.predict(x_test)

mse=mean_squared_error(y_test,y_pred1)
mse

input = np.array([[2024, 2, 3, 24, 85, 50, 66, 0]])
prediction = model1.predict(input)
prediction

