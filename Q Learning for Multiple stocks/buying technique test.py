import math
import numpy as np
from scipy.optimize import minimize

stock_prices=[[11.00,12.00,13.00,14.00,13.00,15.00,17.00,16.00,18.00,19.00,20.00],[22.00,23.00,24.00,25.00,24.00,26.00,27.00,28.00,29.00,27.00,30.00],[23.00,25.00,27.00,28.00,33.00,34.00,33.00,36.00,37.00,38.00,35.00]]

#number of stocks
n=3

#count from the tenth day
current_day=10

ratios=[]
ratios_avg=[]


for i in range (0,n):
    ratios.append([])
    
    for j in range (0,10):
        #find ratios of past 10 days using price(t)/price(t-1)
        ratios[i].append(math.log(stock_prices[i][current_day-10+1+j]/stock_prices[i][current_day-10+j]))
    #average the ratios    
    ratios_avg.append(np.average(ratios[i]))
    
#find covariance matrix of ratios
cov_matrix=np.cov(ratios,ddof=0)

#initial weights
init_weights=[.21,.37,.42]

#defining the sharpe ratio objective function
def sharpe_ratio_objective(weight):
    port_return= np.dot(ratios_avg,weight) #portfolio return is matrix multiply of ratios*weights
    
    #portfolio variance is matrix multiply of (matrix multiply of weights*covariance matrix)*weights
    port_var=np.dot(np.dot(weight,cov_matrix),weight) 
    
    port_vol=np.sqrt(port_var)
    sharpe_ratio=port_return/port_vol
    
    return -sharpe_ratio #minus because we actually want to maximize sharpe ratio

#the sum of weights should be equal to 1 (e.g w1+w2+...+wn=1)
def weight_constraint(weight):
    return np.sum(weight) - 1

#the value of each weight should be between 0 and 1
weight_range=(0,1)
weight_bounds=[]
for i in range(n):
    weight_bounds.append(weight_range) 

#scipy solver    
solution= minimize (sharpe_ratio_objective, init_weights, bounds=weight_bounds, constraints={'type':'eq','fun':weight_constraint})

print( solution.x)
print( -sharpe_ratio_objective(solution.x))    