# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 21:59:28 2019

@author: Raiyaan
"""
#For truncating numbers, like making 4.23333333 to 4.23 using truncate(number,3)
def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

csv_files=['inteldata.csv','appledata.csv']
no_of_companies=len(csv_files)
prices=[]
csv_reader=[]

import csv
import random
random.seed( 30 )
import math
import numpy as np
from scipy.optimize import minimize

total_iteration=0
finish_point=15#10



#read dates to an array

dates=[]


with open('dates.csv') as csv_file:
    date_csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in date_csv_reader:
        if line_count!=0:
            dates.append(str(row[0]))
        line_count+=1



                                        
#read gp and square stock values from csv file
for i in range (0,no_of_companies):
    csv_reader.append(0)
    prices.append([])
    with open(csv_files[i]) as csv_file:
        csv_reader[i] = csv.reader(csv_file, delimiter=',')
        line_count = 0
        date_count = 0
        prev_price=0
        for row in csv_reader[i]:
            if line_count == 0:

                line_count += 1
            else:
                
                if dates[date_count] == row[0]:

                    
                    prices[i].append(truncate(float(row[1]),2))
                    prev_price=truncate(float(row[1]),2) #in case of unavailable price for next day, this is needed
                    date_count+=1
                    
                else: #fill the gaps for missing dates
                    while(dates[date_count]!= row[0]):
                        #trying to guess the missing price
                        prev_price= prev_price + truncate(random.uniform(0.6,0.8),3)*(truncate(float(row[1]),2) - prev_price)
                        prices[i].append(prev_price)
                        
                        date_count+=1
                    prices[i].append(truncate(float(row[1]),2))
                    prev_price=truncate(float(row[1]),2) #in case of unavailable price for next day, this is needed
                    date_count+=1
                    
                line_count += 1
"""                
#read gp and square stock values from csv file
for i in range (0,no_of_companies):
    csv_reader.append(0)
    prices.append([])
    with open(csv_files[i]) as csv_file:
        csv_reader[i] = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader[i]:
            if line_count == 0:

                line_count += 1
            else:
                prices[i].append(truncate(float(row[1]),2))
                line_count += 1
                    

"""
#Sells all stocks in hand and converts to cash
def sell(state_array):
    for i in range(0, no_of_companies):
        state_array[2*no_of_companies] += state_array[i]*state_array[no_of_companies+i]
    for i in range(0, no_of_companies):
        state_array[i] = 0



def buy(state_array,iteration_number):


    ratios=[]
    ratios_avg=[]


    for i in range (0,no_of_companies):
        ratios.append([])

        for j in range (0,10):
            #find ratios of past 10 days using price(t)/price(t-1)
            ratios[i].append(math.log(prices[i][iteration_number-10+1+j]/prices[i][iteration_number-10+j]))
        #average the ratios
        ratios_avg.append(np.average(ratios[i]))

    #find covariance matrix of ratios
    cov_matrix=np.cov(ratios,ddof=0)
    #print(cov_matrix)

    #initial weights
    init_weights=[.5,.5]

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
    for i in range(no_of_companies):
        weight_bounds.append(weight_range)

    #scipy solver
    solution= minimize (sharpe_ratio_objective, init_weights, bounds=weight_bounds, constraints={'type':'eq','fun':weight_constraint})
    budgets=[]
    
    #print(solution.x)
    for i in range(no_of_companies):
        budgets.append(state_array[2*no_of_companies]*solution.x[i])	#allocating budget for each company stock according to solution weights




    #Using the money to buy the stocks according to budget selected by weights

    for i in range(no_of_companies):
        while(budgets[i] > state_array[no_of_companies+i]): #Runs until allocated budget is less than price of that stock
             state_array[2*no_of_companies]-=state_array[no_of_companies+i]
             budgets[i]-=state_array[no_of_companies+i]

             state_array[i]+=1



#^Will add a system to buy 1 of the worse share with remaining money

#Get value of all stocks and cash =  Number of each Stock in hand * each Stock price  + Cash in hand
def get_value(state_array):
    value=0
    for i in range(0, no_of_companies):
        value+= state_array[i]*state_array[no_of_companies+i]
    value += state_array[2*no_of_companies]

    return value

#Defining the features

#Feature 0 is Number of Stocks of each asset
def f0(state_array,x):
    number_of_stocks=0
    for i in range(0, no_of_companies):

        number_of_stocks+= state_array[i]

    if x=="b":
        return 0.99*number_of_stocks
    if x=="s":
        return number_of_stocks
    if x=="h":
        return 0.7*number_of_stocks
    

#Feature 1 is Current Stock Price of each asset
def f1(state_array,x):
    price_of_stocks=0
    for i in range(0, no_of_companies):
        price_of_stocks += state_array[no_of_companies+i]
    if x=="b":
        return price_of_stocks
    if x=="s":
        return 0.99*price_of_stocks
    if x=="h":
        return 0.7*price_of_stocks

#Feature 2 is Cash in Hand
def f2(state_array,x):
    cash_in_hand= state_array[2*no_of_companies]
    if x=="b":
        return cash_in_hand/(initial_tk*0.01)
    if x=="s":
        return 0.55*cash_in_hand/(initial_tk*0.01)
    if x=="h":
        return 0.3*cash_in_hand/(initial_tk*0.01)

#check in "Reference screenshots" folder: q value formula.png
def q_value(state_array,action):
    return weight[0]*f0(state_array,action)+weight[1]*f1(state_array,action)+weight[2]*f2(state_array,action)

#returns the action which produces the maximum q value for the state, basically this is a code for finding maximum of 3 numbers, will make better implementation later
def optimal_action(state_array):
    if  total_iteration >= finish_point-5:
        print("Optimal action")

        if(q_value(state_array,"b")> q_value(state_array,"s")):
            if (q_value(state_array,"b")> q_value(state_array,"h")):
                return "b"
            else:
                return "h"
        else:
            if (q_value(state_array,"s")> q_value(state_array,"h")):
                return "s"
            else:
                return "h"
        
    
    else:
        random_no2= random.random()

        if random_no2<0.9:
            #random code
            print("Random action")

            random_no= random.random()
            if random_no<=0.2:
                return "s"
            elif random_no>=0.6:
                return "b"
            else:
                return "h"
            
        else:
            #optimal code
            print("Optimal action")
            if(q_value(state_array,"b")> q_value(state_array,"s")):
                if (q_value(state_array,"b")> q_value(state_array,"h")):
                    return "b"
                else:
                    return "h"
            else:
                if (q_value(state_array,"s")> q_value(state_array,"h")):
                    return "s"
                else:
                    return "h"
            

        
#initially starting with 10000 tk
initial_tk=500000

#discount is 1 according to paper
discount=1

#In paper exploration probability is said to be 0.2, but 0.01 produces better results
exploration=0.0000000001

#We start from day 16, as we should have knowledge of atleast 15 days before buying
iteration=15

#This is the state vector, initially starting with 0 stocks in hand
state=[]
for i in range(0, no_of_companies):
    state.append(0)
for i in range(0,no_of_companies):
    state.append(prices[i][iteration])
state.append(initial_tk)

#(Number of each Stock in hand, Each Stock price, Cash in hand)

#Took 3 random weight values which will be updated by the algorithm
weight=[1,1,1]

#Taking the optimal action of the first state
action= optimal_action(state)

reward_down=reward_up=0

last_year_optimal_reset=0 #checks if reset has been done to act optimally in last year

#Main loop starts here
while(total_iteration<finish_point):
    prev_state=[]
    prev_state=state[:]     #The ":" is very very important, it does deepcopy
    #First we buy, sell or hold, no code block is needed for hold
    if(action=="b"):
        buy(state,iteration)
    if (action=="s"):
        sell(state)

    #We define two variables to store the previous state and action

    prev_action=action
    reward= get_value(state) - initial_tk #Calculating reward according to paper
    if reward>0:
        reward_up+=1
    else:
        reward_down+=1
    #print("Iteration: ",iteration)

    #Then we update the stock prices of the state to the ones of next day
    iteration+=1
    for i in range(0,no_of_companies):
        state[no_of_companies+i]=prices[i][iteration]


    #check in "Reference screenshots" folder: difference.png
    #print('Buy:',q_value(state,"b"),' Hold:',q_value(state,"s"),' Sell:',q_value(state,"h"))
    difference= q_value(prev_state,prev_action) - ( reward + discount* max(q_value(state,"b"),q_value(state,"h"),q_value(state,"s")) )
    #we update the action variable to the next optimal action
    action= optimal_action(state)
    #print("Optimal action: ", action)

    #We update the weights here, check in "Reference screenshots" folder: weight update.png
    weight[0] = weight[0] - exploration * difference* f0(prev_state, prev_action)
    weight[1] = weight[1] - exploration * difference* f1(prev_state, prev_action)
    weight[2] = weight[2] - exploration * difference* f2(prev_state, prev_action)
    if total_iteration<finish_point-1 and iteration>3285: #unless it is last iteration, will iterate only on first 9 years
        
        iteration=15
        
        total_iteration+=1
        state=[]
        for i in range(0, no_of_companies):
            state.append(0)
        for i in range(0,no_of_companies):
            state.append(prices[i][iteration])
        state.append(initial_tk)
        
    
    if total_iteration==finish_point-1: #on last iteration, will reset state in 10th year
        if iteration>3285 and last_year_optimal_reset==0:
            last_year_optimal_reset=1
            state=[]
            for i in range(0, no_of_companies):
                state.append(0)
            for i in range(0,no_of_companies):
                state.append(prices[i][iteration])
            state.append(initial_tk)
        elif iteration > 3650:
            
            total_iteration+=1


        
        



        #(Number of each Stock in hand, Each Stock price, Cash in hand)
    #print("Weights: ",weight)
    print("Total Iteration: ",total_iteration," Date: ",dates[iteration])
    print(state)
    print("Reward: ",reward)
    print(action)
    print("\n")

    
