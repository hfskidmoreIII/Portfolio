# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 14:55:31 2021

@author: hfski
"""
"""Null hypothesis is that the Vaccine wil not signifcantly decrease S and I. 
Alternative hypothesis is that they will signficantly decrease. """


import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import f_oneway
from scipy.stats.stats import pearsonr

# Total population
Population = 10000
# Infected, Recovered, Exposed, Vaccinated and Death values
Infected, Recovered, Vaccinated= 1, 0, 0.01
# Everyone is susceptible to infection initially.
Suseptible = Population - Infected - Recovered-Vaccinated
# Contact rate and mean recovery rate (in 1/days).
contact, mean_recovery = 2/14,1/14 
# A grid of time points (in days)
t = np.linspace(0, 300,300)


# The SIRV model differential equations.
def deriv(y, t, N, contact, mean_recovery):
    S, I, R, V = y
    dSdt = -contact * S * I / N
    dIdt = contact * S * I / N - mean_recovery * I
    dRdt = mean_recovery * I
    dVdt = Vaccinated * S
    return dSdt, dIdt, dRdt, dVdt

# Initial conditions vector
y0 = Suseptible, Infected, Recovered, Vaccinated

ret = odeint(deriv, y0, t, args=(Population, contact, mean_recovery))
S, I, R, V = ret.T

df = pd.DataFrame({
    'suseptible': S,
    'infected': I,
    'recovered': R,
    'Vaccinated': V})


plt.plot(t,S, 'b', lw=3, label="Susceptible")
plt.plot(t,I, 'r', lw=3, label="Infected")
plt.plot(t,R, 'g', lw=3, label="Recovered")
plt.plot(t,V, 'y', lw=3, label="Vaccinated")
plt.grid(True, which="major", color='black', lw=2, ls='-')
plt.ylabel('Population')
plt.xlabel('Days')
plt.legend()


one_test1=f_oneway(S,V)
one_test2=f_oneway(I,V)
one_test3=f_oneway(R,V)

one_test4=f_oneway(S,R)

one_test5=f_oneway(I,R)
one_test6=f_oneway(I,S)



pers1=pearsonr(S,V)
pers2=pearsonr(I,V)
pers3=pearsonr(R,V)

pers4=pearsonr(R,S)

pers5=pearsonr(I,S)
pers6=pearsonr(I,R)


print(one_test1)
print(one_test2)
print(one_test3)
print(one_test4)

print(one_test5)
print(one_test6)

print(pers1)
print(pers2)
print(pers3)
print(pers4)
print(pers5)
print(pers6)

#The graph shows very low suseptiblity, infected and recovered rates as the days go past 200.
#This suggested that the model would be accurate.  
#The lack of p-value for pearson correlation in Vaccine to Suspetible or to Recovered, suggest no significance
#but did show that the infection to Vaccine was signifcant differece, indicating the vaccine rate rising would
#lower the infection rate. The anova tests though was not signifcant. 
#Since the hyptothesis required the vaccine to lower both the suspetiblity and Infection rate, we would fail 
#to reject the null hypothesis due to suspetibilty not being signifcantly lowered.