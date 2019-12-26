# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 21:59:28 2019

@author: Raiyaan
"""
#For truncating numbers, like making 4.23333333 to 4.23 using truncate(number,3)
def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

csv_files=['gpdata.csv','sqdata.csv']
no_of_companies=len(csv_files)
prices=[]
csv_reader=[]

import csv
import random 
total_iteration=0
finish_point=15#10

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

            
#Sells all stocks in hand and converts to cash
def sell(state_array):
    for i in range(0, no_of_companies):
        state_array[2*no_of_companies] += state_array[i]*state_array[no_of_companies+i]  
    for i in range(0, no_of_companies):
        state_array[i] = 0 


"""
Determines which stock is better looking at previous 15 day net change value
The stock which has increased more tk and decreased less tk is the the better one
Then we will buy the better stock in this iteration
"""   
def buy(state_array,iteration_number):
    net_change=[]
    for i in range(0, no_of_companies):
        net_change.append(0)
    #Determining which stock is better
    for j in range(0, no_of_companies):
        for i in range (iteration_number-15, iteration_number):
        
            if(prices[j][i+1]>prices[j][i]):
    		
                net_change[j]+=(prices[j][i+1]-prices[j][i])
    		
            else:	
                net_change[j]-=(prices[j][i]-prices[j][i+1])			
		
		
		
    expensive_stock_index= net_change.index(max(net_change))

    #Using the money to buy the better stock
    
    
    while(state_array[2*no_of_companies] > state_array[no_of_companies+expensive_stock_index]): #Runs until cash in hand is less than price of the better stock
             state_array[2*no_of_companies]-=state_array[no_of_companies+expensive_stock_index]
             state_array[expensive_stock_index]+=1
      


#^Will add a system to buy 1 of the worse share with remaining money       

#Get value of all stocks and cash =  Number of each Stock in hand * each Stock price  + Cash in hand
def get_value(state_array):
    value=0
    for i in range(0, no_of_companies):
        value+= state_array[i]*state_array[no_of_companies+i]  
    value += state_array[2*no_of_companies]
    
    return value

#Defining the features

#Feature 0 is Number of Stocks of each asset, multiplying a random number for each action to normalize value, which is found by testing :3   
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
    if total_iteration >= finish_point-5:
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
            
            random_no= random.random()
            if random_no<=0.2:
                return "s"
            elif random_no>=0.6:
                return "b"
            else:
                return "h"  
        else:
            #optimal code
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
initial_tk=100000

#discount is 1 according to paper
discount=1

#In paper exploration probability is said to be 0.2, but 0.01 produces better results
exploration=0.00000001

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

#Main loop starts here
while(total_iteration<=finish_point):
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
    print("Iteration: ",iteration)
 
    #Then we update the stock prices of the state to the ones of next day  
    iteration+=1
    for i in range(0,no_of_companies):
        state[no_of_companies+i]=prices[i][iteration]


    #check in "Reference screenshots" folder: difference.png   
    print('Buy:',q_value(state,"b"),' Hold:',q_value(state,"s"),' Sell:',q_value(state,"h"))
    difference= q_value(prev_state,prev_action) - ( reward + discount* max(q_value(state,"b"),q_value(state,"h"),q_value(state,"s")) )
    #we update the action variable to the next optimal action
    action= optimal_action(state)
    print("Optimal action: ", action)

    #We update the weights here, check in "Reference screenshots" folder: weight update.png      
    weight[0] = weight[0] - exploration * difference* f0(prev_state, prev_action)
    weight[1] = weight[1] - exploration * difference* f1(prev_state, prev_action)
    weight[2] = weight[2] - exploration * difference* f2(prev_state, prev_action) 
    
    if iteration>2360:
        iteration=15
        total_iteration+=1
        state=[]
        for i in range(0, no_of_companies):
            state.append(0)
        for i in range(0,no_of_companies):
            state.append(prices[i][iteration])
        state.append(initial_tk)
        
        #(Number of each Stock in hand, Each Stock price, Cash in hand)
    print("Weights: ",weight)
    print("Reward: ",reward)
    print('\n')

