from django.shortcuts import render,redirect
from django.http import HttpResponse
from subprocess import run, PIPE
import sys
import json
# import requests
from saiapp.models import Weekchapters,Testchapters
from django.core.files.storage import FileSystemStorage
import os
from random import randint
from .forms import *
from django.contrib.auth import login,authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail,BadHeaderError
import pandas as pd
from django.views import generic
from django.conf import settings
import random
import mysql.connector

posts = [
    { 'author':'Balasubramanian',
      'title':'My First post',
      'Content': 'First posts content from my side.',
      'date_posted':'August 27, 2019'
     },
     {
      'author':'Lakshmi',
      'title':'My Second post',
      'Content': 'How to live happily',
      'date_posted':'August 27, 2019'
    }

]


def welcome(request):
    return render(request,'saiapp/welcome.html')

def home(request):
    context = {
        'posts':posts
    }

    return render(request,'saiapp/home.html',context)

def about(request):
    return render(request,'saiapp/about.html',{"title":"My sairam"})

def wg(request):
    current_details = Weekchapters.objects.get(rollnumber=1)

    return render(request,'saiapp/wg.html',{"title":"My sairam","current_details":current_details})
    
def weekgen(request):
    return render(request,'saiapp/weekgen.html',{"title":"My sairam"})

def external(request):
    inp = request.POST.get('param')

    out= run([sys.executable,'C://wamp64//www//DEMOPROJECT//demoapp//tests.py',inp],shell=False, stdout=PIPE)
    print(out)

    return render(request,'saiapp//about.html',{'data1' :out.stdout})
    

def generatewhatsapp(request):
    inputvalue = ""
    current_details = Weekchapters.objects.get(rollnumber=1)

    inputvalue = request.POST.get('param2')
    print("input value")
    print(inputvalue)
    if inputvalue == None:
        print("Enter the value")
        out1 = "Enter the Group Code"
        return render(request,'saiapp//generatewhatsapp.html',{'value1': out1,'current_details':current_details})
    else:
        
        out1 = run([sys.executable,settings.WATSAPP_GEN,inputvalue],shell=False, stdout=PIPE)
        return render (request,'saiapp//generatewhatsapp.html',{'value1' : out1.stdout})

def callweekgenexception(request):
    inp = request.POST.get('param1')
    out = run([sys.executable,settings.WEEKLY_CHAP_GEN_EXCEPTION,inp],shell=False, stdout=PIPE)
       
    #obj = Weekchapters.objects.all()
    #obj = Testchapters.objects.all()

    #context = {
    #    'Rollnumber' : obj.rollnumber,
    #    'Currentchapters':obj.currentchapters,
    #    'House' : obj.house

    #}
    return HttpResponse(render(request,'saiapp//wg-exception.html',{'data1' :out.stdout}))
    #return render(request,'saiapp//wg.html',{context})
    
def callweekgen(request):
    inp = request.POST.get('param1')

    #out = run([sys.executable,'C://Documents//VIJEY//django-projects//saiparayan//saiapp//weeklychapgen.py',inp],shell=False, stdout=PIPE)
    out = run([sys.executable, 'C://Users//RANJANI PRASAD//source//repos//saiparayan//saiapp//weeklychapgen.py', inp],shell=False, stdout=PIPE)

    #obj = Weekchapters.objects.all()
    #obj = Testchapters.objects.all()

    #context = {
    #    'Rollnumber' : obj.rollnumber,
    #    'Currentchapters':obj.currentchapters,
    #    'House' : obj.house

    #}
    return HttpResponse(render(request,'saiapp//wg.html',{'data1' :out.stdout}))
    #return render(request,'saiapp//wg.html',{context})
    

def Form(request):
    return render(request,'saiapp//form.html',{})


def upload(request):
    formdata = request.POST.get("CheckCompletion")
    # #print(formdata)
    # rnd = randint(0, 100)
    # #file1 = open('C://Users//RANJANI PRASAD//source//repos//saiparayan//saiapp//uploadedfiles/' + str(rnd) + 'p.txt', 'wb')
    # file1 = open(settings.UPLOADED_FILES_PATH +'/'+ str(rnd) + 'p.txt', 'wb')
    # file1.write(formdata.encode('utf-8'))






    #-------------------------------------------------------------------------
    # READ FRO THE TEXT AREA AND PRINT THE OUTPUT DIRECTLY ON THE SCREEN

    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root",
        database="saiparayanam"
    )
    query = "SELECT House,rollnumber,CurrentChapters FROM `weekchapters`"
    options = pd.read_sql_query(query, mydb)

    # print(options)

    mydb.close()

    dbdf = options


    # print("working on  "+ files)
    def remove(string):
        return string.replace(" ", "")


    watsapp_data = formdata #.encode('utf-8')
    print(("watsapp data ========= " +str(watsapp_data)))
    lines_in_data = str(watsapp_data).split("\n")
    # file = open(filename, encoding="utf8")
    # Rollno = 15
    # chapters = "15 16 17"
    chaplist = ["CHAPTER", "CHAPTER NO", "*CHAPTER NO", "*CHAPTER", "CHAPTERS", "*CHAPTERS", "*CHAPTERS NO",
                "*CHAPTER*"]
    nolist = ["no:", "NO:", "No:", "no.", "No.", "NO.",
              "No:-", "no:-", "no-", "No-", "NO-"]
    mroll = 0
    baselist = []
    for line in lines_in_data:
        print(line)
        stripped_line = line.strip()
        if stripped_line.find("House") != 1:
            perline = stripped_line.split(":")
            aa = (perline[0].upper())
            if (aa.find("ROLL") != -1):

                # if (perline[0]).upper() == "ROLL" or perline[0].upper() == "*ROLL":
                getrollnum = perline[-1]
                # print(getrollnum)
                if getrollnum[:3] in nolist:
                    getrollnum = getrollnum[3::]
                if len(getrollnum) > 2:
                    getrollnum = getrollnum[1::]

                mroll = getrollnum
            elif any(x in str(perline[0]).upper() for x in chaplist):
                # (perline[0].upper().find("CHAPTER") in chaplist)
                getchapter = str(perline[-1])
                # print(getchapter)
                if getchapter[:3] in nolist:
                    getchapter = getchapter[3::]
                getchapter = getchapter.strip(' ')
                baselist.append([int(mroll), getchapter, line])
            else:
                mroll = 0

    baselistdf = pd.DataFrame(sorted(baselist), columns=["rollnumber", "readchapters", "chaptercomments"])
    newdf = dbdf.merge(baselistdf, on='rollnumber', how='outer')
    newdf.loc[newdf['CurrentChapters'] != newdf['readchapters'], 'completed'] = 'Not Completed'
    # newdf.loc[pd.notnull(newdf['readchapters']) and (newdf["completed"] == 'Not Completed'),'completed'] = 'check-format issue'
    newdf.loc[pd.notnull(newdf['readchapters']) & (
                newdf["completed"] == 'Not Completed'), 'completed'] = 'check-format issue'
    # newdf.loc[isnull(newdf['readchapters'])] 'Not Completed']

    completedloc = 'C:/Users/RANJANI PRASAD/source/repos/saiparayan/saiapp/completedfiles/'
    filename = str(random.randint(0, 200))
    filename = completedloc + filename + ".xlsx"

    # newdf.to_excel(filename)
    # print(filename)

    #-------------------------------------------------------------------------


    #
    # for count, x in enumerate(request.FILES.getlist("files")):
    #     ab = request.FILES.getlist("files")
    #     myfile = (ab[count])
    #     rnd = randint(0,100)
    #     def uploadprocess(f):
    #         # with open('C://Documents//VIJEY//django-projects//saiparayan//saiapp//uploadedfiles/'+str(rnd)+'p'+str(myfile), 'wb+') as destination:
    #         with open('C://Users//RANJANI PRASAD//source//repos//saiparayan//saiapp//uploadedfiles/' + str(rnd) + 'p' + str(myfile), 'wb+') as destination:
    #
    #             for chunk in f.chunks():
    #                 destination.write(chunk)
    #     uploadprocess(x)
    #out = run([sys.executable,'C://Users//RANJANI PRASAD//source//repos//saiparayan//saiapp//validatecompletion.py'],shell=False, stdout=PIPE)


    # out = run([sys.executable, settings.VALIDATE_COMPLETION_PATH],shell=False, stdout=PIPE)
    # #print(out.stdout)
    # filename = (out.stdout).decode('utf-8')
    # filename = str(filename)
    # # filename = (filename.split("/"))[-1]
    # filename = (filename.split("xlsx"))[0]
    # filename = filename + 'xlsx'
    # #print("filename="+filename)

    #print(out.stdout)
    #df = pd.read_excel("C:/Users/RANJANI PRASAD/source/repos/saiparayan/saiapp/completedfiles/5p5460-01102020.txt43.xlsx")
    #df = pd.read_excel(filename)



    json_records = newdf.reset_index().to_json(orient='records')
    data = []
    data = json.loads(json_records)

    return render(request, 'saiapp//form.html', {'data2': data})

    #return render(request,'saiapp//form.html',{'data2' :out.stdout})
    #return HttpResponse("File(s) uploaded!")





def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.info(request, f"You are now logged in as {username}.")
                return redirect("/saiapp/about")
                # return redirect("/admin/saiapp/")

            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="saiapp/login.html", context={"login_form":form})



def logoutUser(request):
    logout(request)
    return redirect("/saiapp/")


def checkregistrationdetails(request):
    form = RegistrationdetailsForm(request.POST)
    if request.method == 'POST':

        if form.is_valid():
            form.save(commit=True)

            #----------------------------
            # email from admin to teacher
            #-----------------------------

            teacher_email = [form.data.get("TeacherEmail")]
            admin_email = 'ranjani_bs@yahoo.com'
            # to_email = ['ranjani@test.com']
            sub_email = 'Saiapp Registration'
            msg_email = "Thankyou for submitting your details. You will get an email shortly confirming your registration."
            send_mail(sub_email,msg_email,admin_email,teacher_email)



            #----------------------------
            # email to admin
            #-----------------------------

            sub_email = 'New Teacher Registration'
            msg_email = "A new request for teacher registration has been received with the following details \n"
            msg_email += 'Name = ' + form.data.get("TeacherName") + '\n'
            msg_email += 'Email = ' + form.data.get("TeacherEmail") + '\n'
            msg_email += 'Phone number = ' + form.data.get("TeacherPhone") + '\n'
            msg_email += 'Location = ' + form.data.get("TeacherLocation") + '\n'
            msg_email += 'Parayan Group ID = ' + form.data.get("GroupID") + '\n'
            msg_email += 'Parayan Group Name = ' + form.data.get("GroupName") + '\n'

            send_mail(sub_email,msg_email,teacher_email,[admin_email])

            return redirect("/saiapp/")

    return render(request=request, template_name="saiapp/Registrationdetails.html", context={"reg_form": form})




def volunteerlist(request):
    volunteerinfo = volunteer.objects.all()
    context = {"volunteerinfo":volunteerinfo}
    return render(request,'saiapp/volunteers.html',context)



def volunteerdetails(request,volunteerid):

    if request.POST.get("cancel"):
        return redirect('/saiapp/volunteerlist/')
        # volunteerall = volunteer.objects.all()
        # context = {"volunteerinfo": volunteerall}
        # return render(request, 'saiapp/volunteers.html', context)

    if request.POST.get("enrol"):
        url_redirect = "/saiapp/volunteertodevotee/" + str(volunteerid)
        return redirect(url_redirect)


    volunteerinfo = volunteer.objects.get(pk=volunteerid)


    if request.method == 'POST':

        form = volunteerdetailsform(request.POST,instance=volunteerinfo)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/saiapp/volunteerlist/')
            # volunteerall = volunteer.objects.all()
            # context = {"volunteerinfo": volunteerall}
            # return render(request, 'saiapp/volunteers.html', context)

    form = volunteerdetailsform(instance=volunteerinfo)
    context = {"volunteerinfo": volunteerinfo, "volform": form}
    return render(request,'saiapp/volunteerdetails.html', context)



def volunteeradd(request):

    form = volunteerdetailsform()


    if request.method == "POST":
        form = volunteerdetailsform(request.POST)
        if request.POST.get('cancel'):
            return redirect('/saiapp/volunteerlist/')


        if form.is_valid():

            form.save(commit=True)
            return redirect('/saiapp/volunteerlist/')


            # volunteerinfo = volunteer.objects.all()
            # context = {"volunteerinfo": volunteerinfo}
            # return render(request, 'saiapp/volunteers.html', context)

    return render(request,'saiapp/volunteerdetails.html',{"volform":form})


def volunteertodevotee(request,volunteerid):
    volunteerinfo = volunteer.objects.get(pk=volunteerid)

    if request.method == 'POST':

        form = volunteertodevoteeform(request.POST,volunteerid)

        if form.data.get("RollNumber") != None:

            if (int(form.data.get("RollNumber"))< 1 or int(form.data.get("RollNumber")) > 48):
                messages.error(request, "Roll number must be between 1 and 48")

                context = {"voldevform": form, "voldetails": volunteerinfo}
                return render(request, 'saiapp/volunteertodevotee.html', context)
            else:

                if request.POST.get('submit'):
                    # print("hereeee")

                    context = {"voldevform": form, "voldetails": volunteerinfo}
                    return render(request, 'saiapp/volunteertodevotee.html', context)

                if form.is_valid():
                    form.save(commit=True)
                    volunteerinfo.delete()
                    return redirect('/saiapp/volunteerlist/')

    else:

        form = volunteertodevoteeform(initial={"DevName":volunteerinfo.volName, "Location":volunteerinfo.location, "Language":volunteerinfo.language, "phonenumber":volunteerinfo.phonenumber, "email":volunteerinfo.email})

        context = {"voldevform":form,"voldetails":volunteerinfo}
        return render(request,'saiapp/volunteertodevotee.html',context)


