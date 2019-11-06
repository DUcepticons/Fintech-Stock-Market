# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 21:59:28 2019

@author: Raiyaan
"""
#For truncating numbers, like making 4.23333333 to 4.23 using truncate(number,3)
def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

gp_price = []
sq_price = []

#read gp and square stock values from csv file
import csv

with open('gpdata.csv') as csv_file:
    gp_csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in gp_csv_reader:
        if line_count == 0:
            
            line_count += 1
        else:
            gp_price.append(truncate(float(row[1]),2))
            line_count += 1
with open('sqdata.csv') as csv_file:
    sq_csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in sq_csv_reader:
        if line_count == 0:
            
            line_count += 1
        else:
            sq_price.append(truncate(float(row[1]),2))
            line_count += 1
            
            
#Sells all stocks in hand and converts to cash
def sell(state_array):
    state_array[4] += state_array[0]*state_array[2]  
    state_array[4] += state_array[1]*state_array[3]  
    state_array[0] = 0 
    state_array[1] = 0 

"""
Determines which stock is better looking at previous 15 day net change value
The stock which has increased more tk and decreased less tk is the the better one
Then we will buy the better stock in this iteration
"""   
def buy(state_array,iteration_number):
    gp_better=sq_better=0

    #Determining which stock is better
    for i in range (iteration_number-15, iteration_number):
        if(gp_price[i+1]>gp_price[i]):
		
            gp_better+=(gp_price[i+1]-gp_price[i])
		
        else:	
            gp_better-=(gp_price[i]-gp_price[i+1])			
		
        if(sq_price[i+1]>sq_price[i]):
		
            sq_better+=(sq_price[i+1]-sq_price[i])
		
        else:	
            sq_better-=(sq_price[i]-sq_price[i+1])			
		

    #Using the money to buy the better stock
    if(gp_better>sq_better):

         while(state_array[4] > state_array[2]): #Runs until cash in hand is less than price of the better stock
             state_array[4]-=state_array[2]
             state_array[0]+=1
    else:
         while(state_array[4] > state_array[3]):
             state_array[4]-=state_array[3]
             state_array[1]+=1        


#^Will add a system to buy 1 of the worse share with remaining money       

#Get value of all stocks and cash = Number of Stock 1 in hand * Stock 1 price + Number of Stock 2 in hand * Stock 2 price + Cash in hand
def get_value(state_array):
    value = state_array[0]*state_array[2] + state_array[1]*state_array[3]+state_array[4]
    return value

#Defining the features

#Feature 0 is Number of Stocks of each asset, multiplying a random number for each action to normalize value, which is found by testing :3   
def f0(state_array,x):
    number_of_stocks= state_array[0]+state_array[1]  
    
    if x=="b":
        return 0.18*number_of_stocks
    if x=="s":
        return 0.13*number_of_stocks
    if x=="h":
        return 0.11*number_of_stocks

#Feature 1 is Current Stock Price of each asset
def f1(state_array,x):
    price_of_stocks = state_array[2]+state_array[3]  
    if x=="b":
        return 3*price_of_stocks
    if x=="s":
        return 0.2*price_of_stocks
    if x=="h":
        return 1.1*price_of_stocks

#Feature 2 is Cash in Hand
def f2(state_array,x):
    cash_in_hand= state_array[4]  
    if x=="b":
        return (0.2*cash_in_hand)/initial_tk
    if x=="s":
        return (0.01*cash_in_hand)/initial_tk
    if x=="h":
        return (0.11*cash_in_hand)/initial_tk

#check in "Reference screenshots" folder: q value formula.png   
def q_value(state_array,action):
    return weight[0]*f0(state_array,action)+weight[1]*f1(state_array,action)+weight[2]*f2(state_array,action)

#returns the action which produces the maximum q value for the state, basically this is a code for finding maximum of 3 numbers, will make better implementation later
def optimal_action(state_array):
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
initial_tk=10000

#discount is 1 according to paper
discount=1

#In paper exploration probability is said to be 0.2, but 0.01 produces better results
exploration=0.01

#We start from day 16, as we should have knowledge of atleast 15 days before buying
iteration=15 

#This is the state vector, initially starting with 0 stocks in hand
state=[0,0,gp_price[iteration],sq_price[iteration],initial_tk] #(Stock 1 in hand, Stock 2 in hand, Stock 1 price, Stock 2 Price, Cash in hand)
#Took 3 random weight values which will be updated by the algorithm
weight=[100,6,7]

#Taking the optimal action of the first state
action= optimal_action(state)

#Main loop starts here
for i in range (0,100):

    #First we buy, sell or hold, no code block is needed for hold
    if(action=="b"):
        buy(state,iteration)
    if (action=="s"):
        sell(state)

    #We define two variables to store the previous state and action
    prev_state=state[:]     #The ":" is very very important, it does deepcopy
    prev_action=action  
    reward= get_value(prev_state) - initial_tk #Calculating reward according to paper
    print(reward,iteration)
 
    #Then we update the stock prices of the state to the ones of next day  
    iteration+=1
    state[2]=gp_price[iteration]
    state[3]=sq_price[iteration]

    #check in "Reference screenshots" folder: difference.png   
    difference= q_value(prev_state,prev_action) - ( reward + discount* max(q_value(state,"b"),q_value(state,"h"),q_value(state,"s")) )
    #we update the action variable to the next optimal action
    action= optimal_action(state)

    #We update the weights here, check in "Reference screenshots" folder: weight update.png      
    weight[0] = weight[0] - exploration * difference* f0(prev_state, prev_action)
    weight[1] = weight[1] - exploration * difference* f1(prev_state, prev_action)
    weight[2] = weight[2] - exploration * difference* f2(prev_state, prev_action) 
print(state)

