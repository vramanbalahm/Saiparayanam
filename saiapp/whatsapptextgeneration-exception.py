#!C:/Python38/python.exe  
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains

import xlrd
import mysql.connector
import numpy as np
import pandas as pd
import sys

print("Content-Type: text/html\n\n")
# Establish a Mysql connection

# This progams generates the whatsapp text once login into. This will send messages to the respective
#devotee from the whatsapp interface. 

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="saiparayanam"
)

#mydb = mysql.connector.connect(
#  host="posidbinstance.cvziar2hgxah.us-east-1.rds.amazonaws.com",
#  user="admin",
#  password="Omsairam$123",
#  database="saiparayan"
#)



driver = None
#driver = webdriver.Remote('http://localhost:9515', desired_capabilities=DesiredCapabilities.CHROME)
#driver = webdriver.Firefox(executable_path=r'C:/Python38/Lib/site-packages/selenium/webdriver/common/geckodriver.exe')
driver = webdriver.Chrome(executable_path=r'C:/Python38/Lib/site-packages/selenium/webdriver/common/chromedriver.exe')

driver.maximize_window()
#driver = webdriver.Edge(executable_path='MicrosoftWebDriver.exe')
Link = "https://web.whatsapp.com/"
wait = None
# Adds the cookie into current browser context


def whatsapp_login():
    global wait, driver, Link
    #chrome_options = Options()
    #chrome_options.add_argument('--user-data-dir=./User_Data')
    #driver = webdriver.Firefox(executable_path=r'C:/Python38/Lib/site-packages/selenium/webdriver/common/geckodriver.exe')
    driver = webdriver.Chrome(executable_path=r'C:/Python38/Lib/site-packages/selenium/webdriver/common/chromedriver.exe')
    #driver = webdriver.Chrome(options=chrome_options)
    #wait = WebDriverWait(driver, 600)
    wait = WebDriverWait(driver, 100)
    print("SCAN YOUR QR CODE FOR WHATSAPP WEB IF DISPLAYED")
    driver.get(Link)
    driver.maximize_window()

    print("QR CODE SCANNED")

def send_message(grpcode):
    myfirstrn = 1
#    mylastrn = 48
    cursor1 = mydb.cursor()
#    cursor1.execute("SELECT a.rollnumber as Rollnumber,b.DevName as name,b.phonenumber as Phone,a.CurrentChapters as chapters, a.House as house,b.Devconname as contactname from weekchapters a, tdevotees b where a.rollnumber = b.RollNumber and b.GrpID ="+str(grpcode))
#    cursor1.execute("SELECT a.rollnumber as Rollnumber,b.DevName as name,b.phonenumber as Phone,a.CurrentChapters as chapters, a.House as house,b.Devconname as contactname from weekchapters a, devotee b where a.rollnumber = b.RollNumber and b.GrpID ="+str(grpcode))
    cursor1.execute("SELECT a.rollnumber as Rollnumber,b.DevName as name,b.phonenumber as Phone,a.CurrentChapters as chapters, a.House as house,b.Devconname as contactname from weekchapters a, devotee b where a.rollnumber = b.RollNumber and b.GrpID ="+str(grpcode)+" and a.rollnumber >="+str(myfirstrn))
    records = cursor1.fetchall()
    text = "With Baba blessings completed reading my allotted chapters"
    #msgdf = pd.DataFrame(columns=['Text','Name','Roll no','Chapter No','House'])
    for row in records:
        housecolor= ""
        if str(row[4]) == str("Red"):
            #print("Process lines, file_name command_line %s\n"% command_line.encode('utf-8'))  
            housecolor = ":red heart"
            #housecolor = "\u2764"
        elif str(row[4]) == str("Green"):
            housecolor = ":green heart"
            #housecolor = "u'\u1F49A'"
        elif str(row[4]) == str("Blue"):
            housecolor = ":blue heart"
            #housecolor = "u'\u1F499'"
        elif str(row[4]) == str("Yellow"):
            housecolor = ":yellow heart"  
            #housecolor = "u'\u1F49B'"  
        msg = (text+'\n'+ "*"+"Name:"+"*"+" "+str(row[1])+'\n'+"*"+"Roll No:"+"*"+" "+str(row[0])+'\n'+"*"+"Chapter No:"+"*"+" "+row[3]+""+'\n'+"*"+"House :"+"*"+" "+housecolor)
        
        print(msg)
        contactname=str(row[5])
        contactname = contactname.strip()
        print(contactname)
        user_group_xpath = '//span[@title = "{}"]'.format(contactname)
        searchpath = '//*[@id="side"]/div[1]/div/label/div/div[2]'
        flag = True
        while(flag):
            try:
                sleep(2)
                searchmsg = wait.until(EC.presence_of_element_located((By.XPATH, searchpath)))
                #driver.find_element_by_xpath('//*[@id="side"]/div[1]/div/label/div/div[2]')
                searchmsg.send_keys(contactname)
                user = wait.until(EC.presence_of_element_located((By.XPATH, user_group_xpath)))
                user.click()
                flag = False
            except Exception:
                flag = True
        msg_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')

        for part in msg.split('\n'):
            msg_box.send_keys(part)
            #print(part.find('House'))
            if part.find('House') == 1:
                                
                ActionChains(driver).key_down(Keys.ENTER).perform()
            else : 
                
                ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
            sleep(.25)
        driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button').click()
    print("Message send successfully.")
    
if __name__ == "__main__":
    
    print("Now, Web Page Open")
    whatsapp_login()
    grpcode = sys.argv[1]
    #grpcode = 5460
    #grpcode = input('Enter the group code : ')
    # Let us login and Scan
    send_message(int(grpcode))

    sleep(5)
    driver.close()
    driver.quit()