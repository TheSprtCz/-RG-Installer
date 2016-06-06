#!/usr/bin/python
# -*- coding: utf-8 -*-

#Python components
import sys
import os
import time
import urllib2
import urllib
import json
import tarfile
import shutil
import subprocess
import ConfigParser


#Variables
version = "2.1a"
url = "http://www.mirc.cz/"
options = []
new_profiles = []
hashed = {}
config = ConfigParser.ConfigParser()
debugging = False
prefix = "[RG]"
#Getch
class _Getch:
    """Získá jeden znak bez výstupu na obrazovku"""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()
#Functions
def addOption(optionName, optionText, optionDesc, optionType = "default", download = True, install = True, installDir = False,additional_info = {}, unselectedValue = False, selectedValue = True, optionUrl = False):
    if not optionUrl:
        optionUrl = url + optionName + ".tar.gz"
    if not installDir:
        installDir = optionName
    hashed[optionName] = len(options)
    options.append({"optionName": optionName,"text": optionText, "desc": optionDesc,  "value": unselectedValue, "unselected": unselectedValue, "selected": selectedValue, "download": download, "install": install, "url": optionUrl, "installDir": installDir, "type": optionType, "opt": additional_info })

def getOptionbyName(optionName):
    id = hashed[optionName]
    print(id)
    return options[id] 
def getOptionValue(optionName):
    return getOptionbyName(optionName)["value"]
def processOption(option):
    option["value"] = processAnonymousOption( option["text"],  option["selected"],  option["unselected"])
    #write(option["text"] + " A/N")
    #letter = getch()
    #if letter == "a" or letter == "A":
       #write("...vybráno\n")
       #option["value"] = option["selected"]
    #else:
       #write("...nevybráno\n")
def processAnonymousOption(optionText, selectedValue =  True, unselectedValue = False):
    write(optionText + " A/N")
    letter = getch()
    if letter == "a" or letter == "A":
        write("...vybráno\n")
        return selectedValue
    else:
        write("...nevybráno\n")
        return unselectedValue
def processOptions(filterFunction = lambda optionName: True):
    for option in options:
        if filterFunction(option):
            processOption(option)
def extract(name,path):
	file=tarfile.open(name)
	file.extractall(path)
	file.close
def downloadOption(option):
    url = option["url"]
    downloadUrl(url)
def downloadUrl(url):
    file_name = url.split('/')[-1]
    debug(file_name)
    u = urllib2.urlopen(url)
    downloadStream(u, file_name)
def downloadStream(u, file_name):
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print("Stahuji: %s Velikost: %s B" % (file_name, file_size))
    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d B  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print(status),
    f.close()
def downloadAll():
    for option in options:
        if option["download"] and option["value"]:
            downloadOption(option)

def end():
    print("Pro ukončení stiskněte libovolnou klávesu")
    getch()
    exit()
def write(str):
	sys.stdout.write(str)

def debug(text):
    if debugging:
        print("[DEBUG]"+text)
def doAction(actionText,actionFunction):
    write(actionText)
    actionFunction()
    write("...hotovo\n")
def addProfiles(data):
    for profile in new_profiles:
        data["profiles"][profile["name"]] = {u'gameDir': u''+profile["dir"], u'name': u''+profile["name"]+'', u'lastVersionId': u''+profile["forge"]}
    with open('launcher_profiles.json', 'wb') as outfile:
        json.dump(data, outfile, sort_keys = True, indent = 4)
    print("...hotovo")   
#Installer
print("Vítejte v Instalátoru RebelGames.net, vytvořeného uživatelem Sprt ("+version+")")
mainDir=raw_input("\nVlozte cilovou slozku: ")
if not mainDir[0]=="/":
    mainDir=os.getcwd()+"/"+mainDir
if not os.path.isdir(mainDir):
    print("Slozka "+mainDir+" neexistuje, chcete ji vytvořit? A/N ")
    bool=getch()
    if bool=="a" or bool=="A":
        doAction("Vytvářím složku "+mainDir, lambda: os.makedirs(mainDir))
        #os.makedirs(mainDir)
        #print("...hotovo")
    else:
        end()
if not os.path.isdir(mainDir+"/tmp"):
    os.makedirs(mainDir+"/tmp")
if not os.path.isdir(mainDir+"/versions"):
    os.makedirs(mainDir+"/versions")
tempDir = mainDir + "/tmp"

#Kontrola javy
sp = subprocess.Popen(["java", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
java_v=sp.communicate()
[j,java_v]=java_v
pos1=java_v.find('"')
pos2=java_v.rfind('"')
java_v=java_v[pos1+1:pos2]
debug("Verze javy: "+java_v)
if not int(java_v[2])>=7:
    print("\nVaše java("+java_v+") je zastaralá a proto Modpacky B-Paradise nemusí fungovat správně")
    print("Prosím aktualizujte svoji javu na verzi 1.7 nebo vyšší na www.java.com")

#Config downloading
try: 
    response = urllib2.urlopen(url+"rginstaller.ini")
except IOError:
    print("Nepodařilo se stáhnout configuraci instalátoru, zkontrolujte prosím svoje připojení")
    end()
debug("Dostupnost configu zkontrolována")
os.chdir(tempDir)
downloadStream(response, "config.ini")
#Developerské verze
devVersions = processAnonymousOption("Chcete povolit testovací verze modpacků?")

#Options adding
addOption("forge","Chcete nainstalovat Forge?","forge","forge",True,True,mainDir + "/versions")
addOption("libs","Chcete nainstalovat knihovny Forge?","knihovny forge","libs",True,True,mainDir)
#addOption("ser","Chcete přepsat seznamy serverů?","ser",False,False)
   
#Config Processing
config.read("config.ini")
for section in config.sections():
		if not "rg" in section:
		  if not "dev" in section or devVersions:
		      addOption(section,"Chcete nainstalovat modpack "+config.get(section,"description")+"?",config.get(section,"description"),"modpack",True,True,False,{"forge":config.get(section,"forge")})
		      debug("Přidán modpack "+section)
processOptions()
#print json.dumps(options)
downloadAll()
for option in options:
    if(option["install"] and option["value"]):
        dir = option["installDir"]
        if(option["type"] == "modpack"):
            dir = mainDir + "/" + option["installDir"]
            new_profiles.append({"name":prefix + " " + option["desc"],"forge":option["opt"]["forge"],"dir":dir})
            if(os.path.isdir(dir+"/mods")):
                shutil.rmtree(dir+"/mods")
        write("Instaluji "+ option["desc"] +"...")
        sys.stdout.flush()
        extract(option["optionName"]+".tar.gz",dir)
        print("hotovo")
print ""
os.chdir(mainDir)
if os.path.exists(mainDir+"/launcher_profiles.json"):
    write("Přidávání profilů")
    try:
        with open("launcher_profiles.json") as json_file:
            data = json.load(json_file)
    except (ValueError) as e:
        print("Neplatný .json")
        end()
    addProfiles(data)		
elif processAnonymousOption("Nebyl nalezen soubor s profily(launcher_profiles.json), chcete ho vytvořit?"):
    write("\nGeneruji nový launcher_profiles.json")
    data={}
    data["authenticationDatabase"]={}
    addProfiles(data)
write("\nOdstranuji dočasné soubory")
shutil.rmtree(tempDir)
print("...hotovo")
print("\nInstalace kompletní")
end()
