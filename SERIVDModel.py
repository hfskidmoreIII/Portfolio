# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 15:04:22 2021

@author: hfski
"""
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from scipy.stats import f_oneway
from scipy.stats.stats import pearsonr

Population = 10000
# Infected, Recovered, Exposed, Vaccinated and Death values
Infected, Recovered, Exposed, Vaccinated, Death = 1/Population, 1, 1, 0.01, .01
# Everyone else, S0, is susceptible to infection initially.
Suseptible = Population - Exposed - Infected - Recovered-Vaccinated-Death
# Contact rate, and mean recovery rate, (in 1/days).
contact, Mean_Recovery, sigma, alpha, pheta = 2/14,1/14,14,0.5,2/100 
# A grid of time points (in days)
t = np.linspace(0, 300, 300) #Model runs through 300 days


# The SEIRVD model
def deriv(y, t, Population, contact, Mean_Recovery, sigma, alpha, pheta):
    S, E, I, R, V, D = y
    dSdt = -contact * I * S/ Population
    dEdt = contact * I * S/Population-sigma*E
    dIdt = sigma * E-(1-alpha) * Mean_Recovery * I-alpha*pheta*I
    dRdt = (1-alpha)* Mean_Recovery * I
    dVdt = Vaccinated * S
    dDdT =alpha*pheta*I
    return dSdt, dEdt, dIdt, dRdt, dVdt, dDdT

# Initial conditions vector
y0 = Suseptible, Infected, Recovered, Exposed, Vaccinated, Death
# Integrate the SEIRVD equations over the time grid, t.
ret = odeint(deriv, y0, t, args=(Population, contact, Mean_Recovery,sigma, alpha, pheta))
S, E, I, R, V, D = ret.T

plt.plot(t,S, 'b', lw=3, label="Susceptible")
plt.plot(t,E, 'y', lw=3, label="Exposed")
plt.plot(t,I, 'r', lw=3, label="Infected")
plt.plot(t,V, 'Orange', lw=3, label="Vaccinated")
plt.plot(t,R, 'g', lw=3, label="Recovered")
plt.plot(t,D, 'purple', lw=3, label="Death")
plt.grid(True, which="major", color='black', lw=2, ls='-')
plt.ylabel('Population')
plt.xlabel('Days')
plt.legend()


one_test1=f_oneway(S,V)
one_test2=f_oneway(E,V)
one_test3=f_oneway(I,V)
one_test4=f_oneway(R,V)
one_test5=f_oneway(D,V)


one_test6=f_oneway(S,R)
one_test7=f_oneway(S,E)
one_test8=f_oneway(S,D)

one_test9=f_oneway(I,E)
one_test10=f_oneway(I,S)
one_test11=f_oneway(I,R)

one_test12=f_oneway(E,R)
one_test13=f_oneway(E,D)


pers1=pearsonr(S,V)
pers2=pearsonr(E,V)
pers3=pearsonr(I,V)
pers4=pearsonr(R,V)
pers5=pearsonr(D,V)

pers6=pearsonr(S,R)
pers7=pearsonr(S,E)
pers8=pearsonr(S,D)

pers9=pearsonr(I,E)
pers10=pearsonr(I,S)
pers11=pearsonr(I,R)
pers12=pearsonr(E,R)
pers13=pearsonr(E,D)




print(one_test1)
print(one_test2)
print(one_test3)
print(one_test4)

print(one_test5)
print(one_test6)
print(one_test7)
print(one_test8)
print(one_test9)
print(one_test10)
print(one_test11)
print(one_test12)
print(one_test13)


print(pers1)
print(pers2)
print(pers3)
print(pers4)
print(pers5)
print(pers6)
print(pers7)
print(pers8)
print(pers9)

print(pers10)
print(pers11)
print(pers12)
print(pers13)


#The graph suggests that suggests that over time the number of susceptible, exposed, infected and deaths will go down
#as people recover and get vaccinated. 
#The P value for the ANOVAs though only show the susceptible to recovered to be significant. 
# The P Value for Pearson correlation suggests that there is a positive correlation between  suspetible and recovery, as well as 
#correlational data for infection and vaccinated.
#The data suggests that the graph's results are not satistically signifciant in regards of susceptibility 
#lowering due to vaccination. This is the last model that seems to take in all accounts of a realistic model 
#given the extra component of death rate. 
#We can conclude from the model that further data is needed, for logically, it would seem, lower suspetibility 
# would have lower infected rates that are present. 
 