import pandas as pd
import numpy as np
import csv
# import xlrd
# import mysql.connector
import random
import re
import os

#connecting database and fetching the expected chapters. 
# This program is to check the completion status of the parayan reading.
''' commented by me
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    port='3306',
    database="saiparayanam"
)
'''

#mydb = mysql.connector.connect(
#  host="posidbinstance.cvziar2hgxah.us-east-1.rds.amazonaws.com",
#  user="admin",
#  password="Omsairam$123",
#  database="saiparayan"
#)

query = "SELECT House,rollnumber,CurrentChapters FROM `weekchapters`"
options = pd.read_sql_query(query,mydb)

#print(options)    

mydb.close()

dbdf = options

dirloc = 'C:/Documents/VIJEY/django-projects/saiparayan/saiapp/uploadedfiles'
entries = os.listdir(dirloc)

#print(entries)
for files in entries:
  print("working on  "+ files)
  def remove(string):
      return string.replace(" ", "")


  with open(dirloc+'/'+files, encoding="utf8") as a_file:
  #file = open(filename, encoding="utf8")
  #Rollno = 15
  #chapters = "15 16 17"
    chaplist = ["CHAPTER","CHAPTER NO","*CHAPTER NO", "*CHAPTER", "CHAPTERS", "*CHAPTERS", "*CHAPTERS NO","*CHAPTER*"]
    nolist = ["no:", "NO:", "No:", "no.", "No.", "NO.",
        "No:-", "no:-", "no-", "No-", "NO-"]
    mroll = 0
    baselist = []
    for line in a_file:
      stripped_line = line.strip()
      if stripped_line.find("House") != 1:
        perline = stripped_line.split(":")
        aa = (perline[0].upper())
        if (aa.find("ROLL") != -1):
         
        #if (perline[0]).upper() == "ROLL" or perline[0].upper() == "*ROLL":
            getrollnum = perline[-1]
            #print(getrollnum)
            if getrollnum[:3] in nolist:

                getrollnum = getrollnum[3::]
            if len(getrollnum) > 2:
              getrollnum = getrollnum[1::]

            mroll = getrollnum
        elif any(x in str(perline[0]).upper() for x in chaplist): 
            #(perline[0].upper().find("CHAPTER") in chaplist)
            getchapter = str(perline[-1])
            #print(getchapter)
            if getchapter[:3] in nolist:

                getchapter = getchapter[3::]
            getchapter = getchapter.strip(' ')
            baselist.append([int(mroll), getchapter, line])
        else:
           mroll = 0

  baselistdf = pd.DataFrame(sorted(baselist), columns=["rollnumber", "readchapters","chaptercomments"])
  newdf = dbdf.merge(baselistdf, on='rollnumber', how='outer')
  newdf.loc[newdf['CurrentChapters'] != newdf['readchapters'], 'completed'] = 'Not Completed'
  #newdf.loc[pd.notnull(newdf['readchapters']) and (newdf["completed"] == 'Not Completed'),'completed'] = 'check-format issue'
  newdf.loc[pd.notnull(newdf['readchapters']) & (newdf["completed"] == 'Not Completed'), 'completed'] = 'check-format issue'
  #newdf.loc[isnull(newdf['readchapters'])] 'Not Completed']

  #print(newdf)
  completedloc = 'C:/Documents/VIJEY/django-projects/saiparayan/saiapp/completedfiles/'
  filename = str(random.randint(0, 200))
  filename = completedloc+files+filename+".xlsx"
  newdf.to_excel(filename)
  print("Completed this file " +filename)
  #newdf.to_csv("mynewdf.csv", index=False)
