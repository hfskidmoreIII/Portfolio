
"""
Bank renege example

Covers:

- Resources: Resource
- Condition events

Scenario:
  A counter with a random service time and customers who renege. Based on the
  program bank08.py from TheBank tutorial of SimPy 2. (KGM)

"""
import random
import pandas as pd
import simpy
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats.stats import pearsonr as p
from scipy.stats import f_oneway
RANDOM_SEED = 42
NEW_CUSTOMERS = 20 # Total number of customers
INTERVAL_CUSTOMERS = 2.0  # Generate new customers roughly every x seconds
MIN_PATIENCE = 1  # Min. customer patience
MAX_PATIENCE = 2  # Max. customer patience


def source(env, number, interval, counter):
    """Source generates customers randomly"""
    for i in range(number):
        c = customer(env, 'Customer%02d' % i, counter, time_in_pharm=12.0)
        env.process(c)
        t = random.expovariate(1.0 / interval)
        yield env.timeout(t)


def customer(env, name, counter, time_in_pharm):
    """Customer arrives, is served and leaves."""
    arrive = env.now
    print('%7.4f %s: Here I am' % (arrive, name))

    with counter.request() as req:
        patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)
        results = yield req | env.timeout(patience)

        wait = env.now - arrive

        if req in results:
            print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))

            tib = random.expovariate(1.0 / time_in_pharm)
            yield env.timeout(tib)
            print('%7.4f %s: Finished' % (env.now, name))

        else:
            print('%7.4f %s: RENEGED after %6.3f' % (env.now, name, wait))


# Setup and start the simulation
print('Pharm renege')
random.seed(RANDOM_SEED)
env = simpy.Environment()

# Start processes and run
counter = simpy.Resource(env, capacity=1)
env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter))
env.run()

data = {'customer_finished':[3.8595, 0, 4.9509, 3.1079,0,0,0,11.2816,0,0,22.5667,0,0,0,0,0,0,0,0,0],
        'customer_reneged': [0, 1.736,0,1.027,0,1.220,1.006,1.698,1.698,
                             1.155,1.337,0,1.807,1.536,1.379,1.829,1.862,1.705,1.080,1.228], }

df = pd.DataFrame(data,
                  index=pd.Index(['1','2','3','4','5','6','7','8','9','10','11','12','13', '14','15',
                                 '16', '17','18','19','20'], name= 'customers'),
                  columns=pd.Index(['customer_finished','customer_reneged'], name='Customer Actions'))




custom_plot=df.plot(kind='line', legend=True, figsize=(9,7))
custom_plot.set_xlabel("Customers")
custom_plot.set_ylabel("Finished or Reneged")
custom_plot.grid('black')

S=(df['customer_finished'])
X=(df['customer_reneged'])
one_test=f_oneway(S,X)
p1=p(S,X)
print(p1)
print(one_test)