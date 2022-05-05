#!C:/Python38/python.exe
#algo for weekly chaptergeneration 
#1. Date will be the input. 
#2. The chapter for rollnumber 1 will be given as an input. 
#The logic goes this way
#setting the value of endchapter 
#importing numpy
#import numpy as np

print("Content-Type: text/html\n\n")

import sys
import xlrd
import mysql.connector
import pandas as pd
from datetime import date

# Establish a Mysql connection
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="root",
    port='3306',
    database="saiparayanam"
)

#mydb = mysql.connector.connect(
#  host="posidbinstance.cvziar2hgxah.us-east-1.rds.amazonaws.com",
#  user="admin",
#  password="Omsairam$123",
#  database="saiparayan"
#)


def checkchapter(vchapter1,vendchapter):
    vcurrentchapter=""
    vchapter1 = int(vchapter1)
    prelist = [15,42]
    fulllist = [43,18]

    if int(vchapter1) == vendchapter:
        vcurrentchapter = str(vchapter1)+"(Epilogue)* till Arati" +","+"1"                   
    else: 
        #if (int(vchapter1) == 15 or int(vchapter1) == 42 or int(vchapter1) == 43 or int(vchapter1) == 18):
        if (int(vchapter1) in prelist):
            vcurrentchapter = str(vchapter1)+","+ str(vchapter1+1)+"-"+str(vchapter1+2)
        elif vchapter1 in fulllist:
            vcurrentchapter = str(vchapter1)+"-"+str(vchapter1+1)+","+str(vchapter1+2)
        elif vchapter1==16:
            vcurrentchapter = str(vchapter1)+"-"+str(vchapter1+1)+","+str(vchapter1+2)+"-"+str(vchapter1+3)
        elif vchapter1==50:
            vcurrentchapter = str(vchapter1)+","+str(vchapter1+1)+"(Epilogue)* till Arati"
        else:
            vcurrentchapter = str(vchapter1)+","+str(vchapter1+1)
    #print(vcurrentchapter)
    return(vcurrentchapter)
                

#chapter1 = input("Enter 1st Chapter for Rollnumber 1  ")
chapter1 = sys.argv[1]
endchapter = 51
pardate = str(date.today()) # "2020/06/19"

querylist = []

#insquery = Insert into weekchapters#(rollnumber,currentchapter,parayandate,house,prevchapters,Genstatus,gendate)
#               values (%s,%s,%s,%s,%s,%s,%s)
insquery =""
insquery = "Insert into weekchapters (rollnumber,currentchapters,parayandate,house,Genstatus,gendate)"
i = 1
while i < 49:
    #print(i)
    if i == 1:
        currentchapter = checkchapter(chapter1,endchapter)
        rollnumber = 1
        parayandate = pardate
        housecolor = "Red"
        Genstatus = 1
        getdate = pardate
        val = " values"+" ("+str(rollnumber)+","+"'"+str(currentchapter)+"'"+","+"'"+parayandate+"'"+","+"'"+housecolor+"'"+","+str(Genstatus)+","+ "'"+str(getdate)+"'"+")"
        #print(val)
        querylist.append(insquery+val)       
    else:
        rollnumber = i
        currentchapter = checkchapter(chapter1,endchapter)
        parayandate = pardate
        if i >= 2 and i<= 12:
            housecolor = "Red"
        elif i > 12 and i<= 24:
            housecolor = "Blue"
        elif i > 24 and i<= 36:
            housecolor = "Green"
        else:
            housecolor = "Yellow"
        Genstatus = 1
        getdate = pardate
        val = " values"+" ("+str(rollnumber)+","+"'"+str(currentchapter)+"'"+","+"'"+parayandate+"'"+","+"'"+housecolor+"'"+","+str(Genstatus)+","+ "'"+str(getdate)+"'"+")"
        #print(val)
        querylist.append(insquery+val)       
    chapter1 = int(chapter1)
    chapter1 = chapter1 + 1
    if chapter1 in [44,17,19]:
        chapter1 = chapter1 + 1
    if chapter1 > 51:
       chapter1 = 1
    i += 1
else:
    print("Database updated!")
#inserting records to the table from the array
#print(querylist)
cursor = mydb.cursor()
cursor.execute("DELETE FROM `weekchapters` WHERE 1")
for x in range(0,48):
    #print(querylist[x])
    cursor.execute(querylist[x])
    #cursor.execute(insquery, val)

cursor.close()

#commit transaction
mydb.commit()
#sql = "SELECT rollnumber,currentchapters,house FROM `weekchapters`"
#df = pd.read_sql(sql, mydb)
#mylist = df.values.tolist()
#dfhtml = df.to_html()
#print(dfhtml)
#print(mylist)
#print(df[["rollnumber","CurrentChapters","House"]])

#close the database connection
mydb.close()
