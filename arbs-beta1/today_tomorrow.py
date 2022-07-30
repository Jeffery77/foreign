# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 06:50:15 2019

@author: Duke Young
"""
import re
import datetime
from position import o

def today_tomorrow1():
    x = datetime.datetime.now()


    today = datetime.datetime.today()
    tomorrow = today + datetime.timedelta(1)
    date1 = x.strftime("%d")
    date2 = tomorrow.strftime("%d")
    ndate1 = re.sub("^0+","",date1)
    ndate2 = re.sub("^0+","",date2)
    num =o(int(ndate1))
    num2 =o(int(ndate2))
    pri=(x.strftime("%A")  +", " + num  + " " + x.strftime("%B"))
    pri2=(tomorrow.strftime("%A") + ", " + num2 + " " + tomorrow.strftime("%B"))
    return pri,pri2
#Trial of work