import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.stats.stats import pearsonr
from scipy.stats import f_oneway
#There has been many deaths in Florida due to illness. While many believe it to be covid-19 alone, 
#there may be other works contributing. Data will be mined and analyized to see if any particular illness
#contributes to the death rate. The null hypothesis is there is no illness with any statistical signifigance 
#between the death rate and the illness. The alternative hypothesis would be that there is a significance between the rate
#and at least one illness.import simpy

df=pd.read_excel(r'C:\Users\hfski\Documents\Covid_Location.xlsx', sheet_name='Sheet1')
print(df)

coviddeaths=df['COVID-19 Deaths']
totaldeaths=df['Total Deaths']
pneumonia=df['Pneumonia Deaths']
pneumoniacovid=df['Pneumonia and COVID-19 Deaths']
influenzadeaths=df['Influenza Deaths']
allillness=df['Pneumonia, Influenza, or COVID-19 Deaths']
rcParams['figure.figsize']=10,6

df.plot()
plt.grid()
plt.xlabel("All Places of Death")
plt.ylabel("Death Numbers")
plt.legend(loc=1);

one_test1=f_oneway(coviddeaths,totaldeaths)
one_test2=f_oneway(pneumonia,totaldeaths)
one_test3=f_oneway(pneumoniacovid,totaldeaths)
one_test4=f_oneway(influenzadeaths,totaldeaths)
one_test5=f_oneway(allillness,totaldeaths)

pers1=pearsonr(coviddeaths,totaldeaths)
pers2=pearsonr(pneumonia,totaldeaths)
pers3=pearsonr(pneumoniacovid,totaldeaths)
pers4=pearsonr(influenzadeaths,totaldeaths)
pers5=pearsonr(allillness,totaldeaths)

print(one_test1)
print(one_test2)
print(one_test3)
print(one_test4)
print(one_test5)
print(pers1)
print(pers2)
print(pers3)
print(pers4)
print(pers5)

#Data seems to suggest that there is a positive correlation of significance with all illnesses. 
#However, only one Anova was significant, for influenza deaths. Despite this, we would reject the null hypothesis. 