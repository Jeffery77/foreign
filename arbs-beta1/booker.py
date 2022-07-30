# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 16:00:47 2020

@author: Duke Young
"""
def books(bookmakers):
    c = bookmakers
    d=c.split(",")
    print(d)
    for index, l in enumerate(d):
        if 'B3'in d[index]:
            d[index] = "Bet365"
        elif 'SK' in d[index]:
            d[index] = "Skybet"
        elif 'LD' in d[index]:
            d[index] = "Ladbrokes"
        elif 'WH' in d[index]:
            d[index] = "William Hill"
        elif 'MR' in d[index]:
            d[index] = "Marathon Bet"
        elif 'FB' in d[index]:
            d[index] = "Betfair Sportsbook"
        elif 'VC' in d[index]:
            d[index] = "Bet Victor"
        elif 'PP' in d[index]:
            d[index] = "Paddy Power"
        elif 'UN' in d[index]:
            d[index] = "Unibet"
        elif 'CE' in d[index]:
            d[index] = "Coral"
        elif 'FR' in d[index]:
            d[index] = "Betfred"
        elif 'WA' in d[index]:
            d[index] = "Betway"
        elif 'SA' in d[index]:
            d[index] = "Sports Nation"
        elif 'BY' in d[index]:
            d[index] = "Boyle Sports"
        elif 'VT' in d[index]:
            d[index] = "VBet"
        elif 'OE' in d[index]:
            d[index] = "10Bet"
        elif 'SO' in d[index]:
            d[index] = "SportingBet"
        elif 'EE' in d[index]:
            d[index] = "888sport"
        elif 'Yp' in d[index]:
            d[index] = "Moplay"
        elif 'SX' in d[index]:
            d[index] = "Spreadex"
        elif 'RZ' in d[index]:
            d[index] = "Redzone"
        elif 'BF' in d[index]:
            d[index] = "Betfair"
        elif 'BD' in d[index]:
            d[index] = "Betdaq"
        elif 'MA' in d[index]:
            d[index] = "Matchbook"
        elif 'MK' in d[index]:
            d[index] = "Smarkets"
    z=','.join(map(str,d))
    return z
        
        
        
        
        
        
        
            
            #print("Bet365")
   
    
   
    
#kerei = ['girl','eakon']

#kerei[0] = 'kareshi'

#print(kerei)
    
    