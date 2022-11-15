from django.views.decorators.csrf import csrf_exempt
from pathlib import Path
import os
import shutil
from os import listdir
from zipfile import ZipFile
from .settings import BASE_DIR
from django.shortcuts import render
from django.http import HttpResponse
import json
import subprocess
import threading
import re

class scriptThread (threading.Thread):
    def __init__(self, path):
        threading.Thread.__init__(self)
        self.path = path
    def run(self):
        p = self.path.replace("\\", "/")
        print(p)
        subprocess.run(p, shell= True)

def home(request):
    files = listdir(os.path.join(BASE_DIR ,"static\\html"))
    return render (request,"home.html", context={"files": files})

    
@csrf_exempt 
def search(request):
    
    files = []
    path = "//10.128.3.120/cortex/prod/pdf/ADM/DEMANDE_IMPRESSION/prevoir" 
    dirs = listdir(path) 
    for file in dirs:
        if os.path.isdir(os.path.join(path, file)):
            files.append(file)
    files_stored = list(reversed(files)) 
    last_file = files_stored[0] 
    
    
    if (Path('//10.128.3.120/cortex/prod/pdf/ADM/DEMANDE_IMPRESSION/prevoir/'+last_file+'/AOG_REJEU_'+last_file+'.zip').is_dir()):
        shutil.rmtree('//10.128.3.120/cortex/prod/pdf/ADM/DEMANDE_IMPRESSION/prevoir/'+last_file+'/AOG_REJEU_'+last_file+'.zip')


    if request.POST.get('rech',default=None) != None: 
        query = request.POST.get('rech',default=None) 
        querys = query.split(",")
        list_query = []
        for q in querys:
            qf = query_found(q) 
            list_query.append(qf)        
        list_fileJ7 = [] 
        listOfiles = []
        pdf_found = []
        
        i = 0
        while (i<7):
            list_fileJ7.append(files_stored[i])
            i = i+1
                
        for file in list_fileJ7:
            for archive in listdir(os.path.join(path, file)):
                if archive ==  "ASSURONE_" + file +".zip" :
                    with ZipFile(os.path.join(path, file,archive), 'r') as zipObj:
                        listOfiles.append(zipObj.namelist())
        
        for query in list_query:     
            for archive in listOfiles:
                for fileName in archive :
                    if query.query in fileName:
                        query.found = True
                        pdf_found.append(fileName)
                        
                        
        for file in list_fileJ7:
            for archive in listdir(os.path.join(path, file)):
                if archive ==  "ASSURONE_" + file +".zip" :
                    with ZipFile(os.path.join(path, file,archive), 'r') as zipObj:
                        listOfFileNames  = zipObj.namelist()
                        for pdf in pdf_found:
                            for f in listOfFileNames:
                                if pdf==f:
                                    zipObj.extract(f, os.getcwd() +"/tmp/"+file)
                                    
        results = []
        for date in (listdir(os.getcwd() + "/tmp/")) :
            instence = file_date(date)
            for file in (listdir(os.getcwd() + "/tmp/"+date)) :
                instence.files.append(file)
            results.append(instence)
        
        return render (request, "filtre.html", context={"files": results, "list_query" :list_query,"path" :path})

    if request.POST.get('archive',default=None) != None:
        upload = request.POST.get('archive',default=None)
        zipObj = ZipFile('//10.128.3.120/cortex/prod/pdf/ADM/DEMANDE_IMPRESSION/prevoir/'+last_file+'/AOG_REJEU_'+last_file+'.zip', 'w')
        for date in listdir(os.getcwd()+"/tmp"):
            for fileChild in listdir(os.getcwd()+"/tmp/" +date):
                zipObj.write(os.getcwd()+"/tmp/"+ date + "/"+ fileChild, arcname=fileChild)
                
        zipObj.close()
        html = "<a href= './'><img src = '/./static/images/RETOUR.jpg'/></a><br><p style ='margin-left:30px; font-size: 15px;'>archivé (PATH = //10.128.3.120/cortex/prod/pdf/ADM/DEMANDE_IMPRESSION/prevoir/"+last_file+"/AOG_REJEU_"+last_file+".zip)</p>"
        return HttpResponse(html)

        
@csrf_exempt
def upload(request):
    if len(listdir(os.getcwd()+"/tmp/")) != 0:
        for date in listdir(os.getcwd()+"/tmp/"):
            shutil.rmtree(os.getcwd()+"/tmp/"+date)
    return render(request, 'getpdf.html')
    
    
class file_open():
    def  __init__(self, file):
        self.file = file
        self.linerr = ""
class file_date():
    def  __init__(self, date):
        self.date = date
        self.files =[]

class data_dict():
    def  __init__(self):
        self.script_path = ""
        self.script_name = ""
        self.script_image = ""
        
class query_found():
    def  __init__(self, query):
        self.query = query
        self.found = False

def logpaths(request):
    files = listdir("D:/scripts/log")
    list_file = []
    for file in files:
        ff = file_open(file)
        f = open("D:/scripts/log/"+ff.file).readlines()
        for line in f:
            if "[ERROR" in line:
                ff.linerr = ff.linerr + line + "\n"
        list_file.append(ff)
    return render (request, "logfiles.html", context={"files": files, "objects":list_file})

@csrf_exempt
def scripts_run(request):
    data_list = []

    with open('config.json') as jsonFile:
        data = json.load(jsonFile)

        for item in data["scripts"]:
            dt = data_dict()
            dt.script_path = (item["script_path"])
            dt.script_name = (item["script_name"])
            dt.script_image = (item["script_image"])
            data_list.append(dt)
 
    return render(request, "scriptsexe.html", context={"data": data_list})
 

@csrf_exempt
def scripts_exec(request, path):
    execute = scriptThread(path)
    execute.start()
    return HttpResponse("<popup><p>run</p></popup>")