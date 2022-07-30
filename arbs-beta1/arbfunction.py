 # -*- coding: utf-8 -*
"""
Created on Sun Dec 22 09:00:51 2019

@author: Duke Young
"""

import mysql.connector
mydb = mysql.connector.connect(
        host="localhost",
        user = "root",
        database = "test_db"
        )

mycursor = mydb.cursor()

#li={'id': 4, 'names': 'Sheffield Wednesday v West Brom - Total Goals Over/Under-Over 0.5/ Under 0.5', 'Team1': '1.07', 'Bookmaker1': 'Bet365,Betfair,Coral,Betfair Sportsbook,GN,William Hill', 'Team2': '10.5', 'Bookmaker2': 'Betfair,888sport,Unibet', 'url': 'https://www.oddschecker.com/football/english/championship/sheffield-wednesday-v-west-brom/total-goals-over-under', 'profi': 17.01824655095683, 'n1': 'Over 0.5', 'n2': 'Under 0.5', 'lilen': 2,'Event':'soccer','Market':'sports','Time':'5:50'}

#li ={'Event':"Barcelona vs Chelsea","Market":"Soccer","Time":"8:40","Team1":"Barcelona","Odd1":4.5,"Team2":"Chelsea","Odd2":5.4,"Profit":5,"Market_type":"sports","Id":1,"lilen":2}
def arb_opp(li):
    if li['lilen'] == 3:
       
    
        sqlformula = "INSERT INTO arbfinals(Event,Market,Time,Team1,Odd1,Team2,Odd2,DrawOdd3,Odd3,Profit,Market_type,Id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        arb_opportunity1 = (li['Event'],li['Market'],li['Time'],li['Team1'],li['Odd1'],li['Team2'],li['Odd2'],li['DrawOdd3'],li['Odd3'],li['Profit'],li['Market_type'],li['Id'])

        #print(li)
        mycursor.execute(sqlformula,arb_opportunity1)
        mydb.commit()
        
         
    if li['lilen'] == 2:
        
        sqlformula = "INSERT INTO arbfinals(Event,Market,Time,Team1,Odd1,Team2,Odd2,Profit,Market_type,Id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        arb_opportunity1 = (li['Event'],li['Market'],li['Time'],li['Team1'],li['Odd1'],li['Team2'],li['Odd2'],li['Profit'],li['Market_type'],li['Id'])
            
        mycursor.execute(sqlformula,arb_opportunity1)
        mydb.commit()
        print("Inserted successfully")
        #print(li)
            
            
def delete_arb(ing):
    sql = f"DELETE FROM arb7 WHERE id ={ing}"
    mycursor.execute(sql)
    mydb.commit()


#arb_opp(li)
