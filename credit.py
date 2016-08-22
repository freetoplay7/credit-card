"""The Credit Card Simulator Code

Author: Jiaxi Kang. Last Modified:October 12, 2015
"""

def initialize():
    '''Initializes all global variables used in the program'''
    
    global cur_balance_owing_intst, cur_balance_owing_recent    #determines the 
                                                                #current balance with/
                                                                #without interest
    
    global last_update_day, last_update_month   #used to track previous 
                                                #simulation dates
                                                
    global current_country, last_country, last_country2 #used to track previous
                                                        #country locations
                                                        
    global card_disabled    #checks for validaty of the card
    global MONTHLY_INTEREST_RATE #given rate of interest per month


    cur_balance_owing_intst = 0
    cur_balance_owing_recent = 0
    
    last_update_day, last_update_month = -1, -1
    
    current_country = None
    last_country = None
    last_country2 = None    
    
    card_disabled = False #card is operational when false
    
    MONTHLY_INTEREST_RATE = 0.05

def date_same_or_later(day1, month1, day2, month2):
    '''Return true if the first date is after or equal to the 
    second date 
    
    Arguements: 
    day1, month1, day2, month 2 - Integer values. Assume valid dates for 
    calendar year of 2016.'''
    
    if month1 > month2: 
        return True
        
    elif month1 == month2 and day1 >= day2:
        return True
    
    else:   #date 1 occurs before date 2
        return False
        
    
def all_three_different(c1, c2, c3):
    '''Return true if and only if all three countries are different. 
    
    Arguements: 
    c1, c2, c3 - String values. Assume inputs are valid country names'''
    
    if c1 != None and c2 != None and c3 != None:    #requires visiting 3 
                                                    #countries first
        
        if c1 != c2 and c1 != c3 and c2 != c3:      #visited three different
                                                    #countries
            return True
    
    else:
        return False
        
def calculate_int(month_difference):
    '''Updates current balance owing with/without interest based on the total
    amount of months that have passed
    
    Arguements:
    month_difference - Positiver integer values'''
    
    global cur_balance_owing_intst, cur_balance_owing_recent
    
    if month_difference >= 1:
        cur_balance_owing_intst *= MONTHLY_INTEREST_RATE + 1 #calculates interest
                                                             #after a month
        
        cur_balance_owing_intst += cur_balance_owing_recent #transfers recent 
                                                            #balance to interest
                                                            #balance
        
        cur_balance_owing_recent = 0                        #need to set recent
                                                            #balance to zero
    
        if month_difference > 1:
            cur_balance_owing_intst *= (MONTHLY_INTEREST_RATE + 1) ** \
            (month_difference - 1)  
            #the above calculates the additional interest after a month of interest
            #has already occured
        
def purchase(amount, day, month, country):
    '''Update balance owing with every purchase. Return error if (1) card is 
    already disabled or (2) purchase in three different countries or (3) a 
    simulation has already been made in a future date. Errors (1) and (2) will 
    disable the card. In addition, it will calculate interest occured from the 
    previous purchase
    
    Arguements: 
    amount - Positive integer value
    day, month - Integer values. Assume valid calendar dates
    country - String values. Assume valid country names'''
    
    global last_update_day, last_update_month
    global current_country, last_country, last_country2
    global card_disabled 
    global cur_balance_owing_intst, cur_balance_owing_recent
    

    last_country2 = last_country #update 3 most recent countries
    last_country = current_country
    current_country = country
    
    if card_disabled == True:  #card is disabled..cannot be used
        return "error"
    
    if date_same_or_later(day, month, last_update_day, last_update_month) == False:
        card_disabled = True                                    #card is now disabled
        return "error"   #simulation made in 
                                                                #past...not possible
    
    if all_three_different(current_country, last_country, last_country2) == True:
        card_disabled = True    #card used in three different countries in a row.
                                #it is now disabled
        return "error"   
    
    
    if last_update_month == -1: #when program is initialized
        last_update_month = month
    
    calculate_int(month - last_update_month)    #update balances to purchase date
    
    cur_balance_owing_recent += amount  
    
    last_update_day = day   #required to update the dates
    last_update_month = month

    
def amount_owed(day, month):
    '''Returns the amount owed as of the inputed date. Returns error if the 
    inputed date is on a date later than the most recent simulation.
    
    Arguements:
    day, month - Positive integer values. Assume valid calendar dates'''
    
    global last_update_day, last_update_month
    global card_disabled 
    global cur_balance_owing_intst, cur_balance_owing_recent

        
    if date_same_or_later(day, month, last_update_day, last_update_month) == False:
        card_disabled = True                                    #card is now disabled
        return "error"                                          #simulation made in 
                                                                #past...not possible
    if last_update_month == -1:
        last_update_month = month
    calculate_int(month -last_update_month)
    
    last_update_day = day
    last_update_month = month
    
    return cur_balance_owing_recent + cur_balance_owing_intst
            
def pay_bill(amount, day, month):
    '''Reduces the total amount owed. Updates current interest and recent balances.
    Returns error if the inputed date is on a date later than the most recent
    simulation.
    
    Arguements:
    amount - Positive integer values
    day,month - Positive integer values. Asume valid calendar dates'''
    
    global last_update_day, last_update_month
    global card_disabled 
    global cur_balance_owing_intst, cur_balance_owing_recent
        
    if date_same_or_later(day, month, last_update_day, last_update_month) == False:
        card_disabled = True                                    #card is now disabled
        return "error"                                          #simulation made in 
                                                                #past...not possible
    
    if last_update_month == -1: #when program is initialized
        last_update_month = month
    
    calculate_int(month - last_update_month)    #update balances to purchase date
    
    if amount > (cur_balance_owing_intst + cur_balance_owing_recent):
        return "error"  #amount paid is greater than amount owed, result in error
        card_disabled = True
        
    if amount >= cur_balance_owing_intst:   #updates balances after payment,
                                            #payment goes first to amount
                                            #accruing interest
        cur_balance_owing_intst = 0
        cur_balance_owing_recent = cur_balance_owing_intst - \
        (amount - cur_balance_owing_intst)
    
    else:
        cur_balance_owing_intst -= amount
        
    last_update_day = day   #required to update the dates
    last_update_month = month
    

#Initialize all global variables outside the main block.
initialize()		
    
if __name__ == '__main__':
    #Describe your testing strategy and implement it below.
    #What you see here is just the simulation from the handout, which
    #doesn't work yet.
    
    #Test initialize function
    initialize()
    print(cur_balance_owing_intst)              #0
    print(cur_balance_owing_recent)             #0
    print(last_update_day)                      #-1
    print(last_update_month)                    #-1
    print(current_country)                      #None
    print(last_country)                         #None
    print(last_country2)                        #None  
    print(card_disabled)                        #False
    print(MONTHLY_INTEREST_RATE)                #0.05
    
    #Sample from handout test
    initialize()
    purchase(80, 8, 1, "Canada")
    print("Now owing:", amount_owed(8, 1))      #80.0
    pay_bill(50, 2, 2)
    print("Now owing:", amount_owed(2, 2))      #30.0     (=80-50)
    print("Now owing:", amount_owed(6, 3))      #31.5     (=30*1.05)
    purchase(40, 6, 3, "Canada")
    print("Now owing:", amount_owed(6, 3))      #71.5     (=31.5+40)
    pay_bill(30, 7, 3)
    print("Now owing:", amount_owed(7, 3))      #41.5     (=71.5-30)
    print("Now owing:", amount_owed(1, 5))      #43.65375 (=1.5*1.05*1.05+40*1.05)
    purchase(40, 2, 5, "France")
    print("Now owing:", amount_owed(2, 5))      #83.65375 
    print(purchase(50, 3, 5, "United States"))  #error    (3 diff. countries in 
                                                #          a row)
                                                
    print("Now owing:", amount_owed(3, 5))      #83.65375 (no change, purchase
                                                #          declined)
    print(purchase(150, 3, 5, "Canada"))        #error    (card disabled)
    print("Now owing:", amount_owed(1, 6))      #85.8364375 
                                                #(43.65375*1.05+40)
    
    #Testing purchase/pay_bill/amount_owed function
    initialize()
    
    purchase(50, 1, 1, "Canada")      
    
    print("Now owing:", amount_owed(1, 1))       #50     amount owed on same 
                                                #       purchase date
    
    purchase(80, 5, 1, "USA")           
    
    print("Now owing:", amount_owed(7, 1))      #130    (50 + 80) testing for 
                                                #       multiple purchases
    
    print("Now owing:", amount_owed(2, 2))      #130    validating grace period
    
    print(purchase(20, 5, 3, "Brazil"))         #error  visiting three different
                                                #       countries
    
    print(purchase(30, 1, 3, "Canada"))         #error  card is already disabled
    
    print ("Now owing:", amount_owed(1, 3))     #136.5  (130) * (1.05)^2
    
    pay_bill(50, 1, 4)                          #       pay bill after month
                                                #       of most recent purchase
    
    print("Now owing:", amount_owed(1, 4))      #93.33  (136.5) * 1.05 - 50
    
    print(pay_bill(100, 2, 4))                  #error  paid more than you should
    
    print(pay_bill(30, 1, 3))                   #error  payment to the past
    
    initialize()
    print("Now owing:", amount_owed(1, 1))      #0      check for initial amount
                                                #       amount owed
    
    purchase(30, 10, 5, "Canada")
    print(amount_owed(3, 3))                    #error  checking in the past,
                                                #       card is disabled
    
    print(purchase(10, 5, 6, "Canada"))         #error  cannot purchase after 
                                                #       card is disabled
    
    initialize()
    purchase(30, 1, 1, "Canada")                
    print("Now owing:", amount_owed(1,2))       #30     checking amount_owed 
                                                #       multiple times with 
                                                #       different months
        
    print("Now owing:", amount_owed(1,3))       #31.50  30 * 1.05
    
    print("Now owing:", amount_owed(1,12))      #48.87  30 * 1.05^10
    
    initialize()
    purchase(100, 1, 1, "Canada")               #       checking amount_owed
                                                #       after multiple payments
                                                #       in different months
    
    pay_bill(20, 1, 2)                          
    print("Now owing:", amount_owed(1, 2))      #80     (100 - 20)
    
    pay_bill(30, 1, 5)                      
    print("Now owing:", amount_owed(1, 5))      #62.61  (80*1.05^3 - 30)
    
    pay_bill(50, 1, 8)                          
    print("Now owing:", amount_owed(1, 8))      #22.48  (62.61*1.05^3 - 50)
    
    initialize()
    purchase(50, 1, 2, "Canada")                #       checking amount_owed
                                                #       after multiple purchases
                                                #       in different months
                                                
    purchase(30, 1, 3, "Canada")        
    print("Now owing:", amount_owed(1, 3))      #80     (30 + 50) grace period
                 
    purchase(60, 2, 4, "Canada")
    print("Now owing:", amount_owed(2, 4))      #142.50 (50*1.05 + 30 + 60)
    
    #Testing for date_same_or_later function
    initialize()
    
    print (date_same_or_later(5, 5, 9, 2))      #True   First month after
                                                #       second month
    
    print (date_same_or_later(1, 1, 30, 12))    #False  First month before
                                                #       second month
    
    print (date_same_or_later(12, 12, 12, 12))  #True   Same dates
    
    print (date_same_or_later(12, 3, 9, 3))     #True   Same month, first day 
                                                #       after second day
    
    print (date_same_or_later(3, 4, 21, 4))     #False  Same month, first day 
                                                #       before second day
    
    
    #Testing for all_three_different function
    initialize()
    
    print (all_three_different("Canada", "Brazil", "Germany"))  #True   Three different
                                                                #       countries
    
    print (all_three_different("Canada", "Brazil", "Canada"))   #None   Two same countries
                                                                
    print (all_three_different("Brazil", "Brazil", "Brazil"))   #None   All same countries
    
    
                                    
                                            