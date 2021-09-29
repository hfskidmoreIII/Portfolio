# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 15:10:37 2021

@author: hfski
"""
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import f_oneway
from scipy.stats.stats import pearsonr

# Total population
Population = 1000
# Infected, Recovered, Exposed,and Vaccinated
Infected, Recovered, Exposed, Vaccinated = 1, 0, .01,.01
# Everyone is susceptible to infection initially.
Suseptible = Population - Exposed - Infected - Recovered-Vaccinated
# Contact rate and mean recovery rate (in 1/days).
contact, mean_recovery, alpha = 2/14, 1/14, 5 
# A grid of time points (in days)
t = np.linspace(0, 300, 300)


# The SIR model differential equations.
def deriv(y, t, N, contact, mean_recovery, alpha):
    S, E, I, R, V = y
    dSdt = -contact * S * I / N
    dEdt = contact* I * S/Population-alpha*E
    dIdt = contact * S * I / N - mean_recovery * I
    dRdt = mean_recovery * I
    dVdt = Vaccinated * S
    return dSdt, dEdt, dIdt, dRdt, dVdt

# Initial conditions vector
y0 = Suseptible, Exposed, Infected, Recovered, Vaccinated
# Integrate the SIR equations over the time grid, t.
ret = odeint(deriv, y0, t, args=(Population, contact, mean_recovery,alpha))
S, E, I, R, V = ret.T

df = pd.DataFrame({
    'suseptible': S,
    'Exposed':E,
    'infected': I,
    'recovered': R})


plt.plot(t,S, 'b', lw=3, label="Susceptible")
plt.plot(t,E, 'y', lw=3, label="Exposed")
plt.plot(t,I, 'r', lw=3, label="Infected")
plt.plot(t,R, 'g', lw=3, label="Recovered")
plt.plot(t,V, 'purple', lw=3, label="Vaccinated")
plt.grid(True, which="major", color='grey', lw=2, ls='-')
plt.ylabel('Population')
plt.xlabel('Days')
plt.legend()

one_test1=f_oneway(S,V)
one_test2=f_oneway(E,V)
one_test3=f_oneway(I,V)
one_test4=f_oneway(R,V)

one_test5=f_oneway(I,E)
one_test6=f_oneway(I,S)
one_test7=f_oneway(I,R)

one_test8=f_oneway(E,R)


pers1=pearsonr(S,V)
pers2=pearsonr(E,V)
pers3=pearsonr(I,V)
pers4=pearsonr(R,V)


pers5=pearsonr(E,I)
pers6=pearsonr(E,S)
pers7=pearsonr(E,R)

pers8=pearsonr(I,S)
pers9=pearsonr(I,R)


print(one_test1)
print(one_test2)
print(one_test3)
print(one_test4)

print(one_test5)
print(one_test6)
print(one_test7)
print(one_test8)


print(pers1)
print(pers2)
print(pers3)
print(pers4)
print(pers5)
print(pers6)
print(pers7)
print(pers8)
print(pers9)

#The graph suggests that as the vaccinated number increases, 
#Susceptible, Infected decrease, thus we would reject the null hypothesis. 
#This is supported by the Pearson Correlation test done on infected and vaccianeed
# and the negative correltion test between susceptible and infected.
#There were however no signifant ANOVA tests, which may suggest this is not the most 
#accuarete model, though more accurate then the SIRV model. 
#Due to the results we would fail to reject the null hypothesis since there is no 
#correlation between the vaccine and susceptilbe.
