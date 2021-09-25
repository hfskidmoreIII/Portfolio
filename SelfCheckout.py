"""
SELF CHECKOUT VS EMPLOYEE CHECKOUT SIMULATION
Scenario:
Self checkout system is being considered to be installed in stores.
Information from the designers, suggest self checkouts will be more productive then employee checkouts, 
given the same parameters and more cost effective. Two simulations are run to see if self checkouts 
are faster, then employee run checkouts.

"""
import random
import matplotlib.pyplot as plt
import pandas as pd
import simpy
import numpy as np
from scipy.stats.stats import pearsonr as p
from scipy.stats import f_oneway
RANDOM_SEED = 42
PT_MEAN = 10.0         # Avg. processing time in minutes
PT_SIGMA = 2.0         # Sigma of processing time
MTTF = 300.0           # Mean time to failure in minutes
BREAK_MEAN = 1 / MTTF  # Param. for expovariate distribution
REPAIR_TIME = 5.0     # Time it takes to repair a Self Checkout in minutes
JOB_DURATION = 30.0    # Duration of other jobs in minutes
NUM_checkouts = 5      # Number of machines in the machine shop
WEEKS = 4              # Simulation time in weeks
SIM_TIME = WEEKS * 7 * 24 * 60  # Simulation time in minutes
user_error = 5.0     # Time it takes to repair computer error
NUM_Employee_checkouts = 5      # Number of machines in the machine shop


def time_per_part():
    return random.normalvariate(PT_MEAN, PT_SIGMA)


def time_to_failure():
    """Return time until next failure for a machine."""
    return random.expovariate(BREAK_MEAN)
class EmployeeCheckout(object):
    def __init__(self, env1, name, techemploy):
        self.env = env
        self.name = name
        self.parts_made = 0
        self.broken = False
        
        self.process = env.process(self.working(techemploy))
        env.process(self.break_machine())

    def working(self, techemploy):
        while True:           
            done_in = time_per_part()
            while done_in:
                try:                    
                    start = self.env.now
                    yield self.env.timeout(done_in)
                    done_in = 0
                except simpy.Interrupt:
                    self.broken = True
                    done_in -= self.env.now - start
                    with repairman.request(priority=1) as req:
                        yield req
                        yield self.env.timeout(user_error)

                    self.broken = False

            # Part is done.
            self.parts_made += 1

    def break_machine(self):
        """Break the machine every now and then."""
        while True:
            yield self.env.timeout(time_to_failure())
            if not self.broken:
                # Only break the machine if it is currently working.
                self.process.interrupt()


def other_jobs(env, techemploy):
    while True:
        # Start a new job
        done_in = JOB_DURATION
        while done_in:
            # Retry the job until it is done.
            # It's priority is lower than that of machine repairs.
            with techemploy.request(priority=2) as req:
                yield req
                try:
                    start = env.now
                    yield env.timeout(done_in)
                    done_in = 0
                except simpy.Interrupt:
                    done_in -= env.now - start


class Machine(object):

    def __init__(self, env, name, repairman):
        self.env = env
        self.name = name
        self.parts_made = 0
        self.broken = False
        self.process = env.process(self.working(repairman))
        env.process(self.break_machine())

    def working(self, repairman):
        while True:
            done_in = time_per_part()
            while done_in:
                try:                
                    start = self.env.now
                    yield self.env.timeout(done_in)
                    done_in = 0  # Set to 0 to exit while loop.

                except simpy.Interrupt:
                    self.broken = True
                    done_in -= self.env.now - start  # How much time left?
                    
                    with repairman.request(priority=1) as req:
                        yield req
                        yield self.env.timeout(REPAIR_TIME)
                        
                    self.broken = False
            
            self.parts_made += 1

    def break_machine(self):
        """Break the machine every now and then."""
        while True:
            yield self.env.timeout(time_to_failure())
            if not self.broken:
                self.process.interrupt()

def other_jobs(env, repairman):
    """The repairman's other (unimportant) job."""
    while True:
        done_in = JOB_DURATION
        while done_in:
           
            with repairman.request(priority=2) as req:
                yield req
                try:
                    start = env.now
                    yield env.timeout(done_in)
                    done_in = 0
                except simpy.Interrupt:
                    done_in -= env.now - start

random.seed(RANDOM_SEED) 

env = simpy.Environment()
techemploy = simpy.PreemptiveResource(env, capacity=1)
empcheckout = [EmployeeCheckout(env, 'employee checkout %d' % i, techemploy)
            for i in range(NUM_Employee_checkouts)]
env.process(other_jobs(env, techemploy))


repairman = simpy.PreemptiveResource(env, capacity=1)
machines = [Machine(env, 'SelfCheckout %d' % i, repairman)
            for i in range(NUM_checkouts)]
env.process(other_jobs(env, repairman))

# Execute!
env.run(until=SIM_TIME)


# Analyis/results
print('Employee checkout results after %s weeks' % WEEKS)
for checkout in empcheckout:
    print('%s checked out %d of customers.' % (checkout.name, checkout.parts_made))

    # Analyis/results
print('self checkout results after %s weeks' % WEEKS)
for machine in machines:
    print('%s checked out %d of customers.' % (machine.name, machine.parts_made))
    
data = {'employcheckout':[3947,3945,3962,3949,3950],
        'selfcheckout': [3970,3943,3960,3972,3964]       }

df = pd.DataFrame(data,
                  index=pd.Index(['1','2','3','4','5'], name= 'Employee or Machine'),
                  columns=pd.Index(['employcheckout','selfcheckout']))
custom_plot=df
plt.show()

            
custom_plot=df.plot(kind='bar', legend=True, figsize=(9,7))
custom_plot.set_xlabel("Customers")
custom_plot.set_ylabel("Finished or Reneged")



custom_plot=df.plot(kind='line', legend=True, figsize=(9,7))
custom_plot.set_xlabel("Customers")
custom_plot.set_ylabel("Finished or Reneged")
custom_plot.grid('black')


custom_plot=df.plot(kind='box', legend=True, figsize=(9,7))
custom_plot.set_xlabel("Customers")
custom_plot.set_ylabel("Finished or Reneged")
custom_plot.grid('black')
# Showing the plot
plt.show()


data = {'employcheckout':[3947,3945,3962,3949,3950],
        'selfcheckout': [3970,3943,3960,3972,3964]       }

df = pd.DataFrame(data,
                  index=pd.Index(['1','2','3','4','5'], name= 'Employee or Machine'),
                  columns=pd.Index(['employcheckout','selfcheckout']))
custom_plot=df
plt.show()

            
custom_plot=df.plot(kind='bar', legend=True, figsize=(9,7))
custom_plot.set_xlabel("Customers")
custom_plot.set_ylabel("Finished or Reneged")



custom_plot=df.plot(kind='line', legend=True, figsize=(9,7))
custom_plot.set_xlabel("Customers")
custom_plot.set_ylabel("Finished or Reneged")
custom_plot.grid('black')


custom_plot=df.plot(kind='box', legend=True, figsize=(9,7))
custom_plot.set_xlabel("Customers")
custom_plot.set_ylabel("Finished or Reneged")
custom_plot.grid('black')
# Showing the plot
plt.show()


S=(df['employcheckout'])
X=(df['selfcheckout'])
one_test=f_oneway(S,X)
p1=p(S,X)
print(p1)
print(one_test)


employlanes=12.75*8*5*5*52#employee salaries for five employees, eight hours a day, at 12.75 an hour, for 52 weeks a year minumium
            #this does not include health insurance costs, as well as vaccation time, or sick time, things that often cause
            #over worked employees and people in a disavantage.
print(employlanes*5)
koisak_lane=30000
print(koisak_lane*5)#expected to last five years each

print(employlanes*5-koisak_lane*5)
#The graphs seeemed to suggest that the there is not much a difference in terms of the numbers of processed customers
#between self and employee checkout. P value analysis does not support these results are reliable though.
#Further data would be needed to buid a better model. 
#Simple math does reveal though that companies could save at least half a million dollars by switching to self checkout. 
#More informtation would be needed in the future to further develop accurate models.