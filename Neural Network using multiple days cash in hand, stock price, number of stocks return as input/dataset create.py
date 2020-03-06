# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 21:59:28 2019

@author: Raiyaan
"""
#For truncating numbers, like making 4.23333333 to 4.23 using truncate(number,3)
def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

csv_files=['gpdata_new.csv','appledata.csv']
no_of_companies=len(csv_files)
prices=[]
csv_reader=[]

import csv
import random
import math
import numpy as np
from scipy.optimize import minimize





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

#Sells all stocks in hand and converts to cash
def sell(state_array):
    
        state_array[2] += state_array[0]*state_array[1]
        state_array[0] = 0



def buy(state_array):

    while(state_array[2] >= state_array[1]): #Runs until allocated budget is less than price of that stock
         state_array[2]-=state_array[1]
         state_array[0]+=1


def get_trend_return(company_no,iteration_number):
    ratios=[]
    ratios_avg=0



    for j in range (0,10):
        #find ratios of past 10 days using price(t)/price(t-1)
        ratios.append(math.log(prices[company_no][iteration_number-10+1+j]/prices[company_no][iteration_number-10+j]))
        #average the ratios
        ratios_avg=np.average(ratios)
        
    return ratios_avg
        
#Get value of all stocks and cash =  Number of each Stock in hand * each Stock price  + Cash in hand
def get_value(state_array):
    value=0

    value+= state_array[0]*state_array[1]
    value += state_array[2]

    return value

        
#initially starting with 10000 tk
initial_tk=100000



#We start from day 16, as we should have knowledge of atleast 15 days before buying
iteration=15

#This is the state vector, initially starting with 0 stocks in hand
state=[]

state.append(0)
state.append(prices[0][iteration])
state.append(initial_tk)
state.append(get_trend_return(0,iteration))
print("State: ",state)
    
#Main loop starts here
while(iteration<3285):
    print(iteration)

    hold_state=state[:] 
    buy_state=state[:] 
    sell_state=state[:]     #The ":" is very very important, it does deepcopy
    rewards=[]

    buy(buy_state)
    sell(sell_state)

    #Then we update the stock prices of the states to the ones of next day
    iteration+=1
    hold_state[1]=buy_state[1]=sell_state[1]=prices[0][iteration]
    hold_state[3]=buy_state[3]=sell_state[3]=get_trend_return(0,iteration)
    #print(hold_state," ",buy_state," ",sell_state)
    rewards.append(get_value(hold_state)) #adding hold reward
    rewards.append(get_value(buy_state)) #adding buy reward
    rewards.append(get_value(sell_state)) #adding sell reward    

    action_index=rewards.index(max(rewards))
    if action_index==0:
        state=hold_state[:]
        print("h")
    elif action_index==1:
        state=buy_state[:]
        print("b")
    elif action_index==2:
        state=sell_state[:]
        print("s")
        




        
        



        #(Number of each Stock in hand, Each Stock price, Cash in hand)
    #print("Weights: ",weight)

    print("State: ",state)
    print("Reward: ",rewards)
    print("\n")

    
