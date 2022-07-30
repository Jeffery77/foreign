# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 17:29:58 2020

@author: Duke Young
"""

import re
import sys
import time
import mysql.connector
from arbfunction import arb_opp,delete_arb
import threading
from today_tomorrow import today_tomorrow1
from booker import books
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException,TimeoutException   
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By




class Arbs:
    def __init__(self,new_urls,arb_urls,arb_opp,id_append,dont_add):
        print("The contructor started")
        
    def over_and_unders(self,driver,wait,over_and_under,n1,n2,arb_urls,arb_opp,id_append,o_id,dont_add,books):
        type_events =[]
        odds = []
        bookmakers =[]
        for o_u in over_and_under:
            if o_u.get_attribute('data-bname')== n1 or o_u.get_attribute('data-bname') ==n2:
                type_events.append(o_u.get_attribute('data-bname'))
                odds.append(o_u.get_attribute('data-best-dig'))
                bookmakers.append(o_u.get_attribute('data-best-bks'))
        teams_or_players =wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="betting-odds"]/div[1]/section/div/div/header/h1')))
        if teams_or_players:
            print(teams_or_players.text)
            print(odds)
            self.arb(teams_or_players.text,odds,bookmakers,arb_urls,arb_opp,id_append,o_id,dont_add,books,driver,wait,n1,n2)
        
    def switch(self,driver,wait,name,name2,date1,date2,arb_urls,arb_opp,id_append,o_id,dont_add,books):
        change_match_drop_down = wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class="select-item selected beta-callout"]')))
        #change_match_drop_down =  driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
        driver.execute_script("arguments[0].click();", change_match_drop_down)
    
        next_click_match,markets_text,markets=self.check_name(driver,wait,name,name2)


        ind = next_click_match -1
        while ind <(len(markets_text)):
            try:
                if markets[ind].text:
                    next_one=driver.find_element_by_link_text((markets[ind]).text)
                    driver.execute_script("arguments[0].click();",next_one)
                    ind = ind +1
                    change_match_or_change_event = wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class = "select-item selected beta-callout"]')))
                    #change_match_or_change_event = driver.find_element_by_xpath('//div[@class = "select-item selected beta-callout"]')
                    if change_match_or_change_event.text == "Change Match": 
                        try:
                            #live = wait.until(EC.presence_of_element_located((By.XPATH,'//span[@class ="no-arrow in-play"]')))
                            live = driver.find_element_by_xpath('//span[@class ="no-arrow in-play"]')
                            if live.text:
                                change_match_drop_down =  driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
                                driver.execute_script("arguments[0].click();", change_match_drop_down)
                        except NoSuchElementException:
                            print("It is not live")
                    
                            date = driver.find_element_by_xpath('//span[@class="date beta-caption4 betam-caption2"]')
                            if date1 in date.text or date2 in date.text:           
                        
                                over_and_under = driver.find_elements_by_xpath('//tr[@class="diff-row handicap-participant evTabRow bc"]')
                                self.over_and_unders(driver,wait,over_and_under,"Over 0.5","Under 0.5",arb_urls,arb_opp,id_append,o_id,dont_add,books)
                                print(date2)
                                self.over_and_unders(driver,wait,over_and_under,"Over 1.5","Under 1.5",arb_urls,arb_opp,id_append,o_id,dont_add,books)
                                self.over_and_unders(driver,wait,over_and_under,"Over 2.5","Under 2.5",arb_urls,arb_opp,id_append,o_id,dont_add,books)
                                self.over_and_unders(driver,wait,over_and_under,"Over 3.5","Under 3.5",arb_urls,arb_opp,id_append,o_id,dont_add,books)
                                change_match_drop_down =  driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
                                driver.execute_script("arguments[0].click();", change_match_drop_down)
                            else:
                                continue
                    elif change_match_or_change_event.text == "Change Event":
                        ind = len(markets_text)
                markets = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//a[@class="select-item beta-callout"]')))
            except StaleElementReferenceException:
                ind = ind + 1
                break
       # markets = driver.find_elements_by_xpath('//a[@class="select-item beta-callout"]'
    
    def check_over_under(self,driver,wait,name,name2,element_name1,date1,date2,arb_urls,arb_opp,id_append,o_id,dont_add,books):
        try:
            driver.get(element_name1)
        
        
            next_match = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="quick-switch-centre"]/div/div[2]/div[1]/div[1]')))
            driver.execute_script("arguments[0].click()",next_match)
        
            #//*[@id="quick-switch-centre"]/div/div[2]/div[2]/div/ul/li[1]/a
            word = "Total Goals Over/Under"
        
            patience = wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="quick-switch-centre"]/div/div[2]/div[2]/div/ul/li[1]/a')))
            if patience:
                lists=driver.find_elements_by_xpath('//a[@class="select-item beta-callout"]')
                for l in lists:
                    if word in l.text:
                        i = lists.index(l)
                        break
                nexto = driver.find_element_by_link_text(lists[i].text)
                print("Hello")
        
        #print(nexto.text)
            driver.execute_script("arguments[0].click()",nexto)
            self.switch(driver,wait,name,name2,date1,date2,arb_urls,arb_opp,id_append,o_id,dont_add,books)
            print("Da baby")
        except TimeoutException:
            print("Over and Under Error handled:",)
        
       
    def check_name(self,driver,wait,name,name2):  
    
        try:
            check_first_element = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="quick-switch-centre"]/div/div[1]/div[2]/div/ul[1]/li[2]/a')))
            if check_first_element:
                markets = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//a[@class="select-item beta-callout"]')))
            #markets = driver.find_elements_by_xpath('//a[@class="select-item beta-callout"]')
            markets_text =[]
   
            for i in markets:
                if i.text:
                    markets_text.append(i.text)
    #print(markets_text)
    #for m in markets:
     #   markets_text1.append(m.text)
    #print(markets_text1)    


    
            for m in markets:
                if name not in m.text or name2 not in m.text:
                    continue
                if name in m.text or name2 in m.text:
                    index=markets.index(m)
                    break
    
            next_clickable_match = index + 1
            print("Size is " + str(len(markets_text)))
            print(markets_text)
   
        except:
            next_clickable_match = 1
            markets_text =["Not available"]
            markets = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//a[@class="select-item beta-callout"]')))
       # markets = driver.find_elements_by_xpath('//a[@class="select-item beta-callout"]')
        
        return next_clickable_match, markets_text,markets
    def scroll_odds(self,next_clickable_match,driver,wait,markets,markets_text,sport,get_webpage,arb_urls,arb_opp,id_apppend,o_id,dont_add,books ):
        while next_clickable_match < len(markets_text) :
            try:
                if markets[next_clickable_match].text:
                    next_one=driver.find_element_by_link_text((markets[next_clickable_match]).text)
                    driver.execute_script("arguments[0].click();",next_one)
                    next_clickable_match = next_clickable_match + 1
                    change_match_or_change_event = driver.find_element_by_xpath('//div[@class = "select-item selected beta-callout"]')
                    if change_match_or_change_event.text == "Change Match": 
                        flag,date1,date2=self.live_or_not(driver,wait,arb_urls,arb_opp,id_append,o_id,dont_add,books)
                        if flag:
                            break
                    elif change_match_or_change_event.text == "Change Event":
                        next_clickable_match =len(markets_text)
                    #change_match_drop_down = driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
                    #driver.execute_script("arguments[0].click()",change_match_drop_down)
                    markets = driver.find_elements_by_xpath('//a[@class="select-item beta-callout"]')
                    print(str(next_clickable_match))
                    print(str(len(markets_text)))
    
    
    
            except NoSuchElementException:
                print("Page got redirected")
                next_clickable_match = next_clickable_match + 1
                try:
                    go_back_to_page = driver.find_element_by_xpath('//*[@id="fixtures"]/div/table/tbody/tr[3]/td[5]/a/span[1]')
                    if go_back_to_page:
                        driver.execute_script("arguments[0].click();",go_back_to_page)
            
                        change_match_drop_down = driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
                        driver.execute_script("arguments[0].click()",change_match_drop_down)
                        markets = driver.find_elements_by_xpath('//a[@class="select-item beta-callout"]')
                except:
                    try:
                        page_not_found = driver.find_element_by_xpath('//*[@id="mc"]/section/div/div/header/h1')
                        if page_not_found:
                            driver.get(sport)
                            go_back_to_page = driver.find_element_by_xpath('//*[@id="fixtures"]/div/table/tbody/tr[3]/td[5]/a/span[1]')
                            if go_back_to_page:
                                driver.execute_script("arguments[0].click();",go_back_to_page)
                            
                                change_match_drop_down = driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
                                driver.execute_script("arguments[0].click()",change_match_drop_down)
                                markets = driver.find_elements_by_xpath('//a[@class="select-item beta-callout"]')
                    except:
                        print("CLicking on the link to refresh the page")
                        get_webpage(sport,driver)
                        self.display_of_all_odds1(sport,driver,wait)
                        self.live_or_not(driver,wait,arb_urls,arb_opp,id_append,o_id,dont_add,books)
                        print(len(markets_text))
                        markets = driver.find_elements_by_xpath('//a[@class="select-item beta-callout"]')
                    
        print(len(markets_text))
        print("last digit is " + str(next_clickable_match))
    
    
    
    def get_webpage(self,sport,driver):
        driver.get(sport)
        #sport = sport
        #a=sport.split('/')
        

        #self.final_word=""
        #for i in range(0,4):
        #    self.final_word = self.final_word+a[i]+"/"
  
        
        #print(self.final_word) 
        

        try:
            close = driver.find_element_by_xpath('//*[@id="promo-modal"]/div[1]/div/span')
            if close:
                driver.execute_script("arguments[0].click();",close)
            
        except:
            pass
        
    def display_of_all_odds(self,driver,wait):
        flag3 =False
        try:
            eleme_name1=wait.until(EC.presence_of_all_elements_located((By.XPATH,'//p[@class="fixtures-bet-name beta-footnote"]')))                                                                                     
    
            if eleme_name1:
                name =  eleme_name1[0].text
                name2 = eleme_name1[1].text
                element = eleme_name1[0]
       

        
            if element:
                driver.execute_script("arguments[0].click();", element)
            element_name1 = driver.current_url
        
        except:
            flag3 = True
            name ="Not available"
            name2 = "Not avialable"
            element_name1 = "Not available at the moment"
        return name,name2,element_name1,flag3
    
    def  display_of_all_odds1(self,sport,driver,wait):
        
        try:

            flag4 =False
        
      
            eleme_name1=wait.until(EC.presence_of_all_elements_located((By.XPATH,'//p[@class="fixtures-bet-name beta-footnote"]')))  
            if eleme_name1:
                name1 =  eleme_name1[0].text
                name3 = eleme_name1[1].text
                element1 = eleme_name1[0]
                
       
            if element1:
                driver.execute_script("arguments[0].click();", element1)
                
            element_name2 = driver.current_url
        #print(element_name2)
           
            if sport  in element_name2:
               
                date = wait.until(EC.presence_of_element_located((By.XPATH,'//span[@class="date beta-caption4 betam-caption2"]')))
                    #date = self.driver.find_element_by_xpath('//span[@class="date beta-caption4 betam-caption2"]')
                dat1,dat2 = today_tomorrow1()
                print(date.text)
                
                print(dat1 + " " + dat2)
                if dat1 in date.text or dat2 in date.text:
                    new_urls.append(sport)
                    
                else:
                    print("The time of match is not within available selected duration we need")
                
        except:
            print("Error occurred in the display_of_all_odds1 method")
            flag4 = True
            name1 ="Not available"
            name3 = "Not avialable"
            element_name2 = "Not available at the moment"
      
        print("*******Active_football_urls*****")
        print(new_urls)
        return name1,name3,element_name2,flag4
    
    def arb(self,names,odds,bookmakers,arb_urls,arb_opp,id_append,o_id,dont_add,books,driver,wait,n1='',n2=''):
        def get_team(text,url):
            url ='https://www.oddschecker.com/football/english/premier-league/tottenham-v-wolves/winner'
            if 'football' in url:
                market = 'soccer'
            if 'Winner' in text:
    
                name = re.findall("(.*)(?:Betting .*)",text)
                market_t = 'Winner'
            elif 'Total Goals' in text:
                name = re.findall("(.*)(?:-.*)",text)
                market ='soccer'
                market_t ='Over and under'
                # print(name[0])
            elif 'Both Teams To Score' in text or 'Both Teams to Score' in text:
                name = re.findall("(.*)(?:-.*)",text)
                market = 'soccer'
                market_t = 'Both Teams To Score'
            elif 'Double Chance'  in text:
                name = re.findall("(.*)(?:-.*)",text)
                market = 'soccer'
                market_t = 'Double Chance'
            elif 'Draw No Bet' in text:
                name = re.findall("(.*)(?:-.*)",text)
                market = 'soccer'
                market_t = 'Draw No Bet'
                
            
                
            print("Event: " + name[0] + "  market is :" + market)
            return name,market,market_t
        def get_Event():
            E = driver.find_element_by_xpath('//*[@id="betting-odds"]/div[1]/section/div/div/header/h1')
            return E.text
    
        if len(odds) == 2:
            odd1 = odds[0]
            odd2 = odds[1]
            book1 = books(bookmakers[0])
            book2 = books(bookmakers[1])
        
            if odd1 != 9999 and odd2 !=9999:
                arb1 = (1 /float(odd1))*100
                arb2 = (1 /float(odd2))*100
    
                total  =arb1 +arb2
                def get_odd():
                    c = get_Event()
                    print("The fucking event is " + c)
                
                    E,M,market_t=get_team(c,url)
           
                    date = driver.find_element_by_xpath('//*[@id="betting-odds"]/div[1]/section/div/div/header/div/div/div/span')
                
                    if id_append:
                        i = id_append.pop(0)
                        dont_add.append(i)
                        if n1 or n2:
                            nam = names + "-" + n1 +"/ " + n2
                             #fixing the name of the Both Teams To Score
                            if nam == "Yes vs No":
                                nam = E[0]
                            li = {'Event':nam,'Market':M,'Time':date.text,'Team1':book1,'Odd1':odd1,'Team2':book2,'Odd2':odd2,'Profit':profit,'Market_type':market_t,'Id':i,'n1':n1,'n2':n2,'lilen':2,'url':url}
                            #li = {'id':i,'names':nam,'Team1':odd1,'Bookmaker1':book1,'Team2':odd2,'Bookmaker2':book2,'url':url,'profi':profit,'n1':n1,'n2':n2,'lilen':2}
                            arb_opp(li)
                            arb_urls.append(li)
                        else:
                            na = names[0] + " vs " + names[1]
                             #fixing the name of the Both Teams To Score
                            if na == "Yes vs No":
                                na = E[0]
                            li = {'Event':na,'Market':M,'Time':date.text,'Team1':book1,'Odd1':odd1,'Team2':book2,'Odd2':odd2,'Profit':profit,'Market_type':market_t,'Id':i,'lilen':2,'url':url}
                            #li = {'id':i,'names':na,'Team1':odd1,'Bookmaker1':book1,'Team2':odd2,'Bookmaker2':book2,'url':url,'profi':profit,'lilen':2}
                            arb_opp(li)
                            arb_urls.append(li)
                    else:
                        try:
                            i = o_id[0]
                            if n1 or n2:
                                nam = names + "-" + n1 +"/ " + n2 
                                 #fixing the name of the Both Teams To Score
                                if nam == "Yes vs No":
                                    nam = E[0]
                                li = {'Event':nam,'Market':M,'Time':date.text,'Team1':book1,'Odd1':odd1,'Team2':book2,'Odd2':odd2,'Profit':profit,'Market_type':market_t,'Id':i,'n1':n1,'n2':n2,'lilen':2,'url':url}
                                #li = {'id':i,'names':nam,'Team1':odd1,'Bookmaker1':book1,'Team2':odd2,'Bookmaker2':book2,'url':url,'profi':profit,'n1':n1,'n2':n2,'lilen':2}
                            else:
                                
                                na = names[0] + " vs " + names[1]
                                 #fixing the name of the Both Teams To Score
                                if na == "Yes vs No":
                                    na = E[0]
                                li = {'Event':na,'Market':M,'Time':date.text,'Team1':book1,'Odd1':odd1,'Team2':book2,'Odd2':odd2,'Profit':profit,'Market_type':market_t,'Id':i,'lilen':2,'url':url}
                                #li ={'id':i,'names':na,'Team1':odd1,'Bookmaker1':book1,'Team2':odd2,'Bookmaker2':book2,'url':url,'profi':profit,'lilen':2}
                        
                            o_id[0] = o_id[0] + 1
                            arb_opp(li)
                            arb_urls.append(li)
                        except:
                            truth = True
                          
                            while truth:
                                if o_id[0] in dont_add:
                                    o_id[0] = o_id[0] + 1
                                else:
                                    truth = False
                            i = o_id[0]
                            if n1 or n2:
                                nam = names + "-" + n1 +"/ " + n2
                                 #fixing the name of the Both Teams To Score
                                if nam == "Yes vs No":
                                    nam = E[0]
                                li = {'Event':nam,'Market':M,'Time':date.text,'Team1':book1,'Odd1':odd1,'Team2':book2,'Odd2':odd2,'Profit':profit,'Market_type':market_t,'Id':i,'n1':n1,'n2':n2,'lilen':2,'url':url}
                                #li = {'id':i,'names':nam,'Team1':odd1,'Bookmaker1':book1,'Team2':odd2,'Bookmaker2':book2,'url':url,'profi':profit,'n1':n1,'n2':n2,'lilen':2}
                            else:
                                na = names[0] + " vs " + names[1]
                                 #fixing the name of the Both Teams To Score
                                if na == "Yes vs No":
                                    na = E[0]
                                li = {'Event':na,'Market':M,'Time':date.text,'Team1':book1,'Odd1':odd1,'Team2':book2,'Odd2':odd2,'Profit':profit,'Market_type':market_t,'Id':i,'lilen':2,'url':url}
                                #li ={'id':i,'names':na,'Team1':odd1,'Bookmaker1':book1,'Team2':odd2,'Bookmaker2':book2,'url':url,'profi':profit,'lilen':2}
                                #li = {'id':i,'names':names[0],'odd1':odd1,'odd2':odd2,'url':url,'profi':profit}
                            arb_opp(li)
                            arb_urls.append(li)
                            o_id[0] = o_id[0] + 1
                        print(li)
            
                       # arb_urls.append(driver.current_url) 
            
          
                if total < 100:
                    overall_stake = 100
                    stake1 = (int(overall_stake) * arb1)/total
                    stake2 = (int(overall_stake) * arb2)/total
                    profit = 100- total
                    url =driver.current_url
                    available = False
                
                    if arb_urls:
                        if n1 and n2:
                            for a in arb_urls:
                                if url in a['url'] and n1 in a['n1'] and n2 in a['n2']:
                                    available = True
                        else:
                            for a in arb_urls:
                                if url in a['url']:
                                    available = True
                        if available:
                            print("Already in the database")
                        else:
                            get_odd()
                        
                                
                    else:
                        get_odd()
                    
                
               
   
                
                
           
                #print(arb_urls)
               
        
                    print("Players playing:")
                    print(names)
                    print("Arb opportunity " + str(profit) )
                    print("Bet to be placed at " + book1)
                    print(stake1)
                    print("Bet to be played at " + book2)
                    print(stake2)
                
               
                else:
                    pass
            else:
                pass
        elif len(odds) == 3:
            c = get_Event()
            print("Event is ", c)
            if "Double Chance" in c:
                odd1 = odds[0]
                odd2 = odds[1]
                odd3 = odds[2]
                name = names[0] + " vs " + names[1]
                
            if "Team To Score First" in c:
                odd1  = odds[0]
                odd2  = odds[1]
                odd3  = odds[2]
                name = names[0] + " vs " + names[1]
       
            if names[2] == "Draw":
                odd1 = odds[0]
                odd2 = odds[1]
                odd3 = odds[2]
                name = names[0] + " vs " + names[1]
            elif names[1] == "Draw":
                odd1 = odds[0]
                odd2 = odds[2]
                odd3 = odds[1]
                name = names[0] + " vs " + names[2]
            if odd1 != 9999 and odd2 != 9999 and odd3 != 9999:
                arb1 =(1/float(odd1))*100
                arb2 =(1/float(odd2))*100
                arb3 =(1/float(odd3))*100
            
                book1 = books(bookmakers[0])
                book2 = books(bookmakers[1])
                book3 = books(bookmakers[2])
            
                total =arb1 + arb2 + arb3
        
        
                if total < 100:
                    overall_stake  = 100
                    stake1 = (int(overall_stake) * arb1)/total
                    stake2 = (int(overall_stake) * arb2)/total
                    stake3 = (int(overall_stake) * arb3)/total
                    profit = 100 - total
                    url = driver.current_url
                
                
                    
                    print("The fucking event is " + c)
                
                    E,M,market_t=get_team(c,url)
                    print(E)
                    print(M)
                    print(market_t)
                    date = driver.find_element_by_xpath('//*[@id="betting-odds"]/div[1]/section/div/div/header/div/div/div/span')
                    print(date.text)
                    available = False
                    if arb_urls:
                        for a in arb_urls:
                        
                            if url in a['url']:
                                print("It is already avalilable")
                                available = True
                        if available:
                            pass
                        else:
                            if id_append:
                                i = id_append.pop(0)
                                dont_add.append(i)
                             
                                li = {'Event':name,'Market':M,'Time':date.text,'Team1':book1,'Odd1':odd1,'Team2':book2,'Odd2':odd2,'DrawOdd3':book3,'Odd3':odd3,'Profit':profit,'Market_type':market_t,'Id':i,'lilen':3,'url':url}
                                #li = {'id':i,'names':name,'Team1':odd1,'Bookmaker1':book1,'Team2':odd2,'Bookmaker2':book2,'Team3':odd3,'Bookmaker3':book3,'url':url,'profi':profit,'lilen':3}
                                arb_opp(li)
                                arb_urls.append(li)
                                print("Dont add" + str(dont_add))
                                
                            
                            else:
                    
                                truth =True
                                while truth:
                                    if o_id[0] in dont_add:
                                        o_id[0] = o_id[0] + 1
                                    else:
                                        truth = False
                                i = o_id[0]
                                li = {'Event':name,'Market':M,'Time':date.text,'Team1':book1,'Odd1':odd1,'Team2':book2,'Odd2':odd2,'DrawOdd3':book3,'Odd3':odd3,'Profit':profit,'Market_type':market_t,'Id':i,'lilen':3,'url':url}
                                #li = {'id':i,'names':name,'Team1':odd1,'Bookmaker1':book1,'Team2':odd2,'Bookmaker2':book2,'Team3':odd3,'Bookmaker3':book3,'url':url,'profi':profit,'lilen':3}
                                arb_opp(li)
                                arb_urls.append(li)
                                print(dont_add)
                        
                                o_id[0] = o_id[0] + 1
                            
                            
                    else:   
                        if id_append:
                            i = id_append.pop(0)
                            dont_add.append(i)
                           
                            li = {'Event':name,'Market':M,'Time':date.text,'Team1':book1,'Odd1':odd1,'Team2':book2,'Odd2':odd2,'DrawOdd3':book3,'Odd3':odd3,'Profit':profit,'Market_type':market_t,'Id':i,'lilen':3,'url':url}
                            #li ={'id':i,'names':name,'Team1':odd1,'Bookmaker1':book1,'Team2':odd2,'Bookmaker2':book2,'Team3':odd3,'Bookmaker3':book3,'url':url,'profi':profit,'lilen':3}
                            arb_opp(li)
                            arb_urls.append(li)
                            print("Dont add" + str(dont_add))
                            
                        else:
                    
                            truth =True
                            while truth:
                                if o_id[0] in dont_add:
                                    o_id[0] = o_id[0] + 1
                                else:
                                    truth = False
                            i = o_id[0]
                      
                            li = {'Event':name,'Market':M,'Time':date.text,'Team1':book1,'Odd1':odd1,'Team2':book2,'Odd2':odd2,'DrawOdd3':book3,'Odd3':odd3,'Profit':profit,'Market_type':market_t,'Id':i,'lilen':3,'url':url}
                            #li = {'id':i,'names':name,'Team1':odd1,'Bookmaker1':book1,'Team2':odd2,'Bookmaker2':book2,'Team3':odd3,'Bookmaker3':book3,'url':url,'profi':profit,'lilen':3}
                            arb_opp(li)
                            arb_urls.append(li)
                            print(dont_add)
                        
                            o_id[0] = o_id[0] + 1
                                
                 
                            
             
            
                    print("Players playing:")
                    print(name)
                    print("Arv opportunity " + str(profit))
                    print("Bet to be placed at " +book1)
                    print(stake1)
                    print("Bet to be placed at " +book2)
                    print(stake2)
                    print("Bet to be placed at " +book3)
                    print(stake3)
                else:
                    pass
    
            else:
                pass

    def live_or_not(self,driver,wait,arb_urls,arb_opp,id_append,o_id,dont_add,books):
        date = wait.until(EC.presence_of_element_located((By.XPATH,'//span[@class="date beta-caption4 betam-caption2"]')))
    
    
        date1,date2 = today_tomorrow1()
        flag = False
        print(date.text)
        try:
            live = driver.find_element_by_xpath('//span[@class ="no-arrow in-play"]')
            if live.text:
                change_match_drop_down =  driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
                driver.execute_script("arguments[0].click();", change_match_drop_down)
    
        except:
            print("It is not live")
            if date1 in date.text or date2 in date.text:
                try:
                    names =[]             
                    odds =[]
                    bookmakers =[]
                    best_odds = driver.find_elements_by_xpath('//tr[@class="diff-row evTabRow bc"]')
                    for best_odd in best_odds:
                        names.append(best_odd.get_attribute('data-bname'))  
                        odds.append(best_odd.get_attribute('data-best-dig'))
                        bookmakers.append(best_odd.get_attribute('data-best-bks'))
                    print(odds)
                    for n in names:
                        print("This is the fucking names of  the matches:" + n)
                    self.arb(names,odds,bookmakers,arb_urls,arb_opp,id_append,o_id,dont_add,books,driver,wait)
                except NoSuchElementException:
                    print("It is not available")
        
                change_match_drop_down =  driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
                driver.execute_script("arguments[0].click();", change_match_drop_down)
            
            
            else:
               flag =True
            
        return flag,date1,date2
    def Both_Teams_To_Score(self,driver,wait,name,name2,date1,date2):
        #//*[@id="quick-switch-centre"]/div/div[2]/div[1]/div[1]
        # events name 
        event_string = "Both Teams To Score"
        event_string2 = "Both Teams to Score"
      
        change_market = driver.find_element_by_xpath('//*[@id="quick-switch-centre"]/div/div[2]/div[1]')
        
        driver.execute_script("arguments[0].click();",change_market)
        print("Beginning of Both Teams to score")
        
        patience = wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="quick-switch-centre"]/div/div[2]/div[2]/div/ul/li[1]/a')))
        if patience:
            lists=driver.find_elements_by_xpath('//a[@class="select-item beta-callout"]')
            for l in lists:
                #print(l.text)
                if event_string == l.text or event_string2 == l.text:
                    i = lists.index(l)
                    break
            event_link = driver.find_element_by_link_text(lists[i].text)
            driver.execute_script("arguments[0].click()",event_link)
            
     # changing events
            change_match_drop_down = wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class="select-item selected beta-callout"]')))
        #change_match_drop_down =  driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
            driver.execute_script("arguments[0].click();", change_match_drop_down)
    
            next_click_match,markets_text,markets=self.check_name(driver,wait,name,name2)
            
            ind = next_click_match -1
            while ind <(len(markets_text)):
                 try:
                      if markets[ind].text:
                          next_one=driver.find_element_by_link_text((markets[ind]).text)
                          driver.execute_script("arguments[0].click();",next_one)
                          ind = ind +1
                          change_match_or_change_event = wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class = "select-item selected beta-callout"]')))
                          #change_match_or_change_event = driver.find_element_by_xpath('//div[@class = "select-item selected beta-callout"]')
                          if change_match_or_change_event.text == "Change Match": 
                                  try:
                                      live = driver.find_element_by_xpath('//span[@class ="no-arrow in-play"]')
                                      if live.text:
                                          change_match_drop_down =  driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
                                          driver.execute_script("arguments[0].click();", change_match_drop_down)
                                  except NoSuchElementException:
                                      print("It is not live")
                                      
                                      date = driver.find_element_by_xpath('//span[@class="date beta-caption4 betam-caption2"]')
                                      if date1 in date.text or date2 in date.text:
                                          try:
                                              names =[]             
                                              odds =[]
                                              bookmakers =[]
                                              best_odds = driver.find_elements_by_xpath('//tr[@class="diff-row evTabRow bc"]')
                                              for best_odd in best_odds:
                                                  names.append(best_odd.get_attribute('data-bname'))  
                                                  odds.append(best_odd.get_attribute('data-best-dig'))
                                                  bookmakers.append(best_odd.get_attribute('data-best-bks'))
                                              print(odds)
                                              for n in names:
                                                  print("This is the fucking names of  the matches:" + n)
                                              self.arb(names,odds,bookmakers,arb_urls,arb_opp,id_append,o_id,dont_add,books,driver,wait)
                                              change_match_drop_down =  driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
                                              driver.execute_script("arguments[0].click();", change_match_drop_down)
                                          except NoSuchElementException:
                                              print("It is not available")
                                              change_match_drop_down =  driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
                                              driver.execute_script("arguments[0].click();", change_match_drop_down)
                                      else:
                                          continue
                          elif change_match_or_change_event.text == "Change Event":
                             ind = len(markets_text)
                      markets = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//a[@class="select-item beta-callout"]')))
                 except StaleElementReferenceException:
                     ind = ind + 1
                     break
                                      
    def Double_Chance(self,driver,wait,name,name2,date1,date2):
        #//*[@id="quick-switch-centre"]/div/div[2]/div[1]/div[1]
        # events name 
        event_string = "Double Chance"
        #event_string2 = "Both Teams to Score"
      
        change_market = driver.find_element_by_xpath('//*[@id="quick-switch-centre"]/div/div[2]/div[1]')
        
        driver.execute_script("arguments[0].click();",change_market)
        print("Beginning of Both Teams to score")
        
        patience = wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="quick-switch-centre"]/div/div[2]/div[2]/div/ul/li[1]/a')))
        if patience:
            lists=driver.find_elements_by_xpath('//a[@class="select-item beta-callout"]')
            for l in lists:
                #print(l.text)
                if event_string == l.text:
                    i = lists.index(l)
                    break
            event_link = driver.find_element_by_link_text(lists[i].text)
            driver.execute_script("arguments[0].click()",event_link)
            
     # changing events
            change_match_drop_down = wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class="select-item selected beta-callout"]')))
        #change_match_drop_down =  driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
            driver.execute_script("arguments[0].click();", change_match_drop_down)
    
            next_click_match,markets_text,markets=self.check_name(driver,wait,name,name2)
            
            ind = next_click_match 
            while ind <(len(markets_text)):
                 try:
                      if markets[ind].text:
                          next_one=driver.find_element_by_link_text((markets[ind]).text)
                          driver.execute_script("arguments[0].click();",next_one)
                          ind = ind +1
                          change_match_or_change_event = wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class = "select-item selected beta-callout"]')))
                          #change_match_or_change_event = driver.find_element_by_xpath('//div[@class = "select-item selected beta-callout"]')
                          if change_match_or_change_event.text == "Change Match": 
                                  try:
                                      live = driver.find_element_by_xpath('//span[@class ="no-arrow in-play"]')
                                      if live.text:
                                          change_match_drop_down =  driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
                                          driver.execute_script("arguments[0].click();", change_match_drop_down)
                                  except NoSuchElementException:
                                      print("It is not live")
                                      
                                      date = driver.find_element_by_xpath('//span[@class="date beta-caption4 betam-caption2"]')
                                      if date1 in date.text or date2 in date.text:
                                          try:
                                              names =[]             
                                              odds =[]
                                              bookmakers =[]
                                              best_odds = driver.find_elements_by_xpath('//tr[@class="diff-row evTabRow bc"]')
                                              for best_odd in best_odds:
                                                  names.append(best_odd.get_attribute('data-bname'))  
                                                  odds.append(best_odd.get_attribute('data-best-dig'))
                                                  bookmakers.append(best_odd.get_attribute('data-best-bks'))
                                              print("Odds")
                                              print(odds)
                                              for n in names:
                                                  print("This is the fucking names of  the matches:" + n)
                                              self.arb(names,odds,bookmakers,arb_urls,arb_opp,id_append,o_id,dont_add,books,driver,wait)
                                              change_match_drop_down =  driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
                                              driver.execute_script("arguments[0].click();", change_match_drop_down)
                                          except NoSuchElementException:
                                              print("It is not available")
                                              change_match_drop_down =  driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
                                              driver.execute_script("arguments[0].click();", change_match_drop_down)
                                      else:
                                          continue
                          elif change_match_or_change_event.text == "Change Event":
                             ind = len(markets_text)
                      markets = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//a[@class="select-item beta-callout"]')))
                 except StaleElementReferenceException:
                     ind = ind + 1
                     break
    
    def Draw_nobet(self,driver,wait,name,name2,date1,date2):
        #//*[@id="quick-switch-centre"]/div/div[2]/div[1]/div[1]
        # events name 
        event_string = "Draw No Bet"
       
      
        change_market = driver.find_element_by_xpath('//*[@id="quick-switch-centre"]/div/div[2]/div[1]')
        
        driver.execute_script("arguments[0].click();",change_market)
        print("Beginning of Both Teams to score")
        
        patience = wait.until(EC.visibility_of_element_located((By.XPATH,'//*[@id="quick-switch-centre"]/div/div[2]/div[2]/div/ul/li[1]/a')))
        if patience:
            lists=driver.find_elements_by_xpath('//a[@class="select-item beta-callout"]')
            for l in lists:
                #print(l.text)
                if event_string == l.text:
                    i = lists.index(l)
                    break
            event_link = driver.find_element_by_link_text(lists[i].text)
            driver.execute_script("arguments[0].click()",event_link)
            
     # changing events
            change_match_drop_down = wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class="select-item selected beta-callout"]')))
        #change_match_drop_down =  driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
            driver.execute_script("arguments[0].click();", change_match_drop_down)
    
            next_click_match,markets_text,markets=self.check_name(driver,wait,name,name2)
            
            ind = next_click_match -1
            while ind <(len(markets_text)):
                 try:
                      if markets[ind].text:
                          next_one=driver.find_element_by_link_text((markets[ind]).text)
                          driver.execute_script("arguments[0].click();",next_one)
                          ind = ind +1
                          change_match_or_change_event = wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class = "select-item selected beta-callout"]')))
                          #change_match_or_change_event = driver.find_element_by_xpath('//div[@class = "select-item selected beta-callout"]')
                          if change_match_or_change_event.text == "Change Match": 
                                  try:
                                      live = driver.find_element_by_xpath('//span[@class ="no-arrow in-play"]')
                                      if live.text:
                                          change_match_drop_down =  driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
                                          driver.execute_script("arguments[0].click();", change_match_drop_down)
                                  except NoSuchElementException:
                                      print("It is not live")
                                      
                                      date = driver.find_element_by_xpath('//span[@class="date beta-caption4 betam-caption2"]')
                                      if date1 in date.text or date2 in date.text:
                                          try:
                                              names =[]             
                                              odds =[]
                                              bookmakers =[]
                                              best_odds = driver.find_elements_by_xpath('//tr[@class="diff-row evTabRow bc"]')
                                              for best_odd in best_odds:
                                                  names.append(best_odd.get_attribute('data-bname'))  
                                                  odds.append(best_odd.get_attribute('data-best-dig'))
                                                  bookmakers.append(best_odd.get_attribute('data-best-bks'))
                                              print(odds)
                                              for n in names:
                                                  print("This is the fucking names of  the matches:" + n)
                                              self.arb(names,odds,bookmakers,arb_urls,arb_opp,id_append,o_id,dont_add,books,driver,wait)
                                              change_match_drop_down =  driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
                                              driver.execute_script("arguments[0].click();", change_match_drop_down)
                                          except NoSuchElementException:
                                              print("It is not available")
                                              change_match_drop_down =  driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
                                              driver.execute_script("arguments[0].click();", change_match_drop_down)
                                      else:
                                          continue
                          elif change_match_or_change_event.text == "Change Event":
                             ind = len(markets_text)
                      markets = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//a[@class="select-item beta-callout"]')))
                 except StaleElementReferenceException:
                     ind = ind + 1
                     break    
                 
   
    
    def Team_to_score_First(self,driver,wait,name,name2,date1,date2):
        #//*[@id="quick-switch-centre"]/div/div[2]/div[1]/div[1]
        # events name 
     
     # changing events
            #change_match_drop_down = wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class="select-item selected beta-callout"]')))
        #change_match_drop_down =  driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
           # driver.execute_script("arguments[0].click();", change_match_drop_down)
    
            next_click_match,markets_text,markets=self.check_name(driver,wait,name,name2)
            
            ind = next_click_match -1
            while ind <(len(markets_text)):
                 try:
                      if markets[ind].text:
                          next_one=driver.find_element_by_link_text((markets[ind]).text)
                          driver.execute_script("arguments[0].click();",next_one)
                          ind = ind +1
                          change_match_or_change_event = wait.until(EC.presence_of_element_located((By.XPATH,'//div[@class = "select-item selected beta-callout"]')))
                          #change_match_or_change_event = driver.find_element_by_xpath('//div[@class = "select-item selected beta-callout"]')
                          if change_match_or_change_event.text == "Change Match": 
                                  try:
                                      live = driver.find_element_by_xpath('//span[@class ="no-arrow in-play"]')
                                      if live.text:
                                          change_match_drop_down =  driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
                                          driver.execute_script("arguments[0].click();", change_match_drop_down)
                                  except NoSuchElementException:
                                      print("It is not live")
                                      ### Team to score first url
                                        
                                      cur = driver.current_url
                                      print("currnent:",cur)

                                      sub_str = cur.rsplit('/',1)

                                      sub_str = sub_str[0] + "/" + "team-to-score-first"
        
                                      driver.get(sub_str)
                                      
                                      date = driver.find_element_by_xpath('//span[@class="date beta-caption4 betam-caption2"]')
                                      if date1 in date.text or date2 in date.text:
                                          try:
                                              names =[]             
                                              odds =[]
                                              bookmakers =[]
                                              best_odds = driver.find_elements_by_xpath('//tr[@class="diff-row evTabRow bc"]')
                                              for best_odd in best_odds:
                                                  names.append(best_odd.get_attribute('data-bname'))  
                                                  odds.append(best_odd.get_attribute('data-best-dig'))
                                                  bookmakers.append(best_odd.get_attribute('data-best-bks'))
                                              print(odds)
                                              for n in names:
                                                  print("This is the fucking names of  the matches:" + n)
                                              self.arb(names,odds,bookmakers,arb_urls,arb_opp,id_append,o_id,dont_add,books,driver,wait)
                                              cur = driver.current_url
                                              print("currnent:",cur)

                                              sub_str = cur.rsplit('/',1)

                                              sub_str = sub_str[0] + "/" + "winner"
        
                                              driver.get(sub_str)
                                              change_match_drop_down =  driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
                                              driver.execute_script("arguments[0].click();", change_match_drop_down)
                                          except NoSuchElementException:
                                              print("It is not available")
                                              change_match_drop_down =  driver.find_element_by_xpath('//div[@class="select-item selected beta-callout"]')
                                              driver.execute_script("arguments[0].click();", change_match_drop_down)
                                      else:
                                          continue
                          elif change_match_or_change_event.text == "Change Event":
                             ind = len(markets_text)
                      ### go back to winner url
                      #cur = driver.current_url
                      #print("currnent:",cur)

                      #sub_str = cur.rsplit('/',1)

                      #sub_str = sub_str[0] + "/" + "winner"
        
                      #driver.get(sub_str)
                      markets = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//a[@class="select-item beta-callout"]')))
                 except StaleElementReferenceException:
                     ind = ind + 1
                     break       
    
    def provide_urls(self):
        driver = webdriver.Chrome('chromedriver')
        wait =WebDriverWait(driver,60)
        
        #sports = ['https://www.oddschecker.com/football/europa-league/']
        #sports = ['https://www.oddschecker.com/football/belgium/jupiler-pro-league', 'https://www.oddschecker.com/football/finland/veikkausliiga', 'https://www.oddschecker.com/football/austria/bundesliga', 'https://www.oddschecker.com/football/belarus/belarus-reserve-league', 'https://www.oddschecker.com/football/world/china/super-league', 'https://www.oddschecker.com/football/germany/3rd-liga', 'https://www.oddschecker.com/football/germany/bundesliga-2', 'https://www.oddschecker.com/football/poland/ekstraklasa', 'https://www.oddschecker.com/football/romania/liga-i', 'https://www.oddschecker.com/football/croatia/1-hnl', 'https://www.oddschecker.com/football/denmark/1st-division', 'https://www.oddschecker.com/football/russia/premier-league', 'https://www.oddschecker.com/football/sweden/superettan', 'https://www.oddschecker.com/football/world/usa/mls']
        
        sports= [  'https://www.oddschecker.com/football/english/championship','https://www.oddschecker.com/football/spain/copa-del-rey',
	'https://www.oddschecker.com/football/english/league-1', 'https://www.oddschecker.com/football/english/league-2', 'https://www.oddschecker.com/football/english/fa-cup',
	'https://www.oddschecker.com/football/elite-coupon', 'https://www.oddschecker.com/football/france/ligue-2',
	'https://www.oddschecker.com/football/europa-league', 'https://www.oddschecker.com/football/womens-coupon','https://www.oddschecker.com/football/germany/bundesliga','https://www.oddschecker.com/football/italy/serie-a',
    'https://www.oddschecker.com/football/spain/la-liga-primera','https://www.oddschecker.com/football/scottish/premiership','https://www.oddschecker.com/football/netherlands/eredivisie','https://www.oddschecker.com/football/netherlands/eerste-divisie','https://www.oddschecker.com/football/italy/serie-b',
    'https://www.oddschecker.com/football/italy/super-cup','https://www.oddschecker.com/football/spain/la-liga-segunda','https://www.oddschecker.com/football/spain/la-liga-segunda-b','https://www.oddschecker.com/football/portugal/segunda-liga'
    'https://www.oddschecker.com/football/poland/ekstraklasa','https://www.oddschecker.com/football/norway/eliteserien','https://www.oddschecker.com/football/poland/cup','https://www.oddschecker.com/football/sweden/allsvenskan',
    'https://www.oddschecker.com/football/switzerland/super-league','https://www.oddschecker.com/football/wales/premier-league','https://www.oddschecker.com/football/world/australia/a-league',
    'https://www.oddschecker.com/football/world/japan/emperors-cup','https://www.oddschecker.com/football/world/tunisia/league-1','https://www.oddschecker.com/football/world/uae/premier-league',
    
    'https://www.oddschecker.com/football/france/ligue-1','https://www.oddschecker.com/football/portugal/league-cup','https://www.oddschecker.com/football/belgium/jupiler-pro-league','https://www.oddschecker.com/football/belgium/division-2','https://www.oddschecker.com/football/cyprus/1-division',
    'https://www.oddschecker.com/football/greece/superleague','https://www.oddschecker.com/football/finland/veikkausliiga','https://www.oddschecker.com/football/hungary/nb1','https://www.oddschecker.com/football/ireland/premier-division',
    'https://www.oddschecker.com/football/scottish/championship','https://www.oddschecker.com/football/austria/bundesliga','https://www.oddschecker.com/football/belarus/belarus-reserve-league','https://www.oddschecker.com/football/world/china/super-league','https://www.oddschecker.com/football/friendlies',
    'https://www.oddschecker.com/football/croatia/cup','https://www.oddschecker.com/football/czech-republic/cup','https://www.oddschecker.com/football/germany/3rd-liga','https://www.oddschecker.com/football/germany/bundesliga-2','https://www.oddschecker.com/football/greece/cup','https://www.oddschecker.com/football/italy/copa-primavera',
    'https://www.oddschecker.com/football/italy/serie-c','https://www.oddschecker.com/football/poland/1-liga','https://www.oddschecker.com/football/poland/ekstraklasa','https://www.oddschecker.com/football/poland/lower-leagues','https://www.oddschecker.com/football/romania/liga-i','https://www.oddschecker.com/football/russia/1-division',
    'https://www.oddschecker.com/football/serbia/superliga','https://www.oddschecker.com/football/turkey/super-lig','https://www.oddschecker.com/football/ukraine/vischaya-league','https://www.oddschecker.com/football/portugal/primeira-liga','https://www.oddschecker.com/football/croatia/1-hnl','https://www.oddschecker.com/football/czech-republic/druha-liga',
    'https://www.oddschecker.com/football/france/ligue-1https://www.oddschecker.com/football/france/ligue-1','https://www.oddschecker.com/football/germany/dfb-pokal','https://www.oddschecker.com/football/austria/lower-leagues","https://www.oddschecker.com/football/belarus/premier-league','https://www.oddschecker.com/football/denmark/1st-division',
    'https://www.oddschecker.com/football/denmark/2nd-division','https://www.oddschecker.com/football/denmark/superligaen','https://www.oddschecker.com/football/ireland/first-division','https://www.oddschecker.com/football/israel/liga-leumit','https://www.oddschecker.com/football/netherlands/eerste-divisiehttps://www.oddschecker.com/football/netherlands/eerste-divisie',
    'https://www.oddschecker.com/football/romania/liga-ii','https://www.oddschecker.com/football/slovenia/1-snl','https://www.oddschecker.com/football/english/non-league/national-league','https://www.oddschecker.com/football/austria/lower-leagues','https://www.oddschecker.com/football/austria/austrian-cup','https://www.oddschecker.com/football/belarus/premier-league',
    'https://www.oddschecker.com/football/czech-republic/synot-liga','https://www.oddschecker.com/football/portugal/segunda-liga','https://www.oddschecker.com/football/russia/premier-league','https://www.oddschecker.com/football/slovakia/super-liga','https://www.oddschecker.com/football/sweden/superettan','https://www.oddschecker.com/football/switzerland/super-league',
    'https://www.oddschecker.com/football/turkey/1-lig','https://www.oddschecker.com/football/turkey/super-lig','https://www.oddschecker.com/football/world/usa/mls'
    
    
    ]

    
        for sport in sports:
            self.get_webpage(sport,driver)
            self.display_of_all_odds1(sport,driver,wait)
    
           
            
            
    def main(self):
       driver1 = webdriver.Chrome('chromedriver')
       wait1 = WebDriverWait(driver1,60)
          
       while True:
           for sp in new_urls:
                print("NEW URLS:")
                print(new_urls)
                self.get_webpage(sp,driver1)
                print("Displaying all the odds page")
                name,name2,element_name1,flag3=self.display_of_all_odds(driver1,wait1)
                print("Name:" + name)
                print("Name:" + name2)
                #if flag is true the rest of the code does not continue and continue with the next element on the for loop
                
                if flag3:
                    continue
                
                flag,date1,date2=self.live_or_not(driver1,wait1,arb_urls,arb_opp,id_append,o_id,dont_add,books)
                print("STAGE 3 COMPLETE")
                #next_clickable_match,markets_text,markets  = self.check_name(driver1,wait1,name,name2)
                #self.scroll_odds(next_clickable_match,driver1,wait1,markets,markets_text,sp,self.get_webpage,arb_urls,arb_opp,id_append,o_id,dont_add,books)
                #print("LAST STAGE COMPLETED")
                #self.check_over_under(driver1,wait1,name,name2,element_name1,date1,date2,arb_urls,arb_opp,id_append,o_id,dont_add,books)
                #self.Both_Teams_To_Score(driver1,wait1,name,name2,date1,date2)
                #self.Double_Chance(driver1,wait1,name,name2,date1,date2)
                #self.Draw_nobet(driver1,wait1,name,name2,date1,date2)
                self.Team_to_score_First(driver1,wait1,name,name2,date1,date2)
             
                
                print("End ****/n/******/n/********")
    
    



if __name__ == "__main__":
    new_urls = []
    arb_urls=[]
    dont_add=[]
    id_append=[4,5]
    o_id = [1]
    a = Arbs(new_urls,arb_urls,arb_opp,id_append,dont_add)
    b = Arbs(new_urls,arb_urls,arb_opp,id_append,dont_add)
    thread1 = threading.Thread(target=a.main)
    thread2 = threading.Thread(target=a.provide_urls)
    
    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()