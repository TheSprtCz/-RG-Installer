#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
#Načtění komponent Pythonu
import os
import time
import urllib2
import urllib
import json
import tarfile
import shutil
import subprocess

#Přípravy
version="1.2b"

#Defaultni hodnoty
ic6=True
ic5=False
eden=True
st=True
forge=True
mmap="r"
ser=True
q=False
urlm="http://www.mirc.cz/"
core7=True
core8=True
apo=True

core7dir=""
ic6dir=""
ic5dir=""
edendir=""
stdir=""
cure7dir=""
core8dir=""
apodir=""
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

#Funkce

def download(url):
    file_name = url.split('/')[-1]
    u = urllib2.urlopen(url)	
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
def downloadq(url,text):
	write("Stahuji "+text)
	name = url.split('/')[-1]
	urllib.urlretrieve (url, name)
	print("...hotovo")
def down(name,quiet,text):
	global urlm
	url=urlm+name
	if not quiet:
		downloadq(url,text)
	else:
		download(url)	
def write(str):
	sys.stdout.write(str)
def read(nmb):
	key=getch()
	return key
def end():
	print("Pro ukončení stiskněte libovolnou klávesu")
	getch()
	os.system('setterm -cursor on')	
	exit()
def minmap(path,mmap):
	if mmap=="r":
		extract("reismm164.tar.gz",path+"/mods","text",True)
	if mmap=="z":
		extract("zansmm164.tar.gz",path+"/mods","text",True)
	if mmap=="m":
		extract("mapwritter164.tar.gz",path+"/mods","text",True)				
def select(text,q):
	write(text+" A/N ")
	letter=read(1)
	if letter=="a" or letter=="A":
		if q==True:
			write("...vybráno")
		print("")
		return True
	else:
		if q==True:
			write("...nevybráno")
		print("")	
		return False
def extract(name,path,text,quiet):
	if not quiet:
		write("Instaluji "+text)
	file=tarfile.open(name)
	file.extractall(path)
	file.close
	if not quiet:
		print("..hotovo")
def serinfo(path,ser):
	if ser:
		shutil.copy2("servers.dat",path)
	else:
		if not os.path.exists(path+"/servers.dat"):
			shutil.copy2("servers.dat",path)
			#print "Kopiruji seznam serveru"
											
#Přeinstalační přípravy
print("Vítejte v Instalátoru B-paradise, vytvořeného uživatelem Sprt ("+version+")")
fdir=raw_input("\nVlozte cilovou slozku: ")
if not fdir[0]=="/":
	fdir=os.getcwd()+"/"+fdir
if not os.path.isdir(fdir):
	print("Slozka "+fdir+" neexistuje, chcete ji vytvořit? A/N ")
	bool=read(1)
	if bool=="a" or bool=="A":
		write("Vytvářím složku "+fdir)
		os.makedirs(fdir)
		print("...hotovo")
	else:
		end()
if not os.path.isdir(fdir+"/tmp"):
	os.makedirs(fdir+"/tmp")
if not os.path.isdir(fdir+"/versions"):
	os.makedirs(fdir+"/versions")
#Kontrola javy
sp = subprocess.Popen(["java", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
java_v=sp.communicate()
[j,java_v]=java_v
pos1=java_v.find('"')
pos2=java_v.rfind('"')
java_v=java_v[pos1+1:pos2]
if not int(java_v[2])>=7:
	print("\nVaše java("+java_v+") je zastaralá a proto Modpacky B-Paradise nemusí fungovat správně")
	print("Prosím aktualizujte svoji javu na verzi 1.7 na www.java.com")
	
#Kontrola launcheru
if not os.path.exists(fdir+"/launcher_profiles.json"):
	jsonl=False
	cjson=select("\nNebyl nalezen soubor s profily(launcher_profiles.json), chcete ho vytvořit?",True)	
else:
	jsonl=True
	cjson=False
	
#Výběr komponent
sel=select("\nChcete použít k instalaci standardní nastavení? (Všechny modpacky, Rei's minimap)",True)
if not sel:
	ic6=select("Chcete nainstalovat IC2 mody?",True)
	ic5=select("Chcete nainstalovat IC2 mody na 1.5.2?",True)
	eden=select("Chcete nainstalovat Eden mody?",True)
	st=select("Chcete nainstalovat SkyTech mody?",True)
	core7=select("Chcete nainstalovat 1.7.2 mody?",True)
	apo=select("Chcete nainstalovat Apocalypsu?",True)
	core8=select("Chcete nainstalovat Core 1.8?",True)
# 	print("Jaky z minimap modu chcete nainstalovat?")
#	write("R-Rei's minimap, Z-Zan's minimap, M-MapWriter, N-Žádný ")
#	let=getch()
#	if let=="r" or let=="R":
#		write("...Rei's minimap")
#		mmap="r"
#	if let=="z" or let=="Z":
#		write("...Zan's minimap")
#		mmap="z"
#	if let=="m" or let=="M":
#		write("...MapWritter")
#		mmap="m"
#	if let=="n" or let=="N":
#		write("...Žádný")
#		mmap="n"
#	print("")  
	forge=select("Chcete nainstalovat Forge a jeho knihovny?",True)				
	ser=select("Chcete přepsat seznamy serverů?",True)
	q=select("Chcete podrobné informace o stahování?",True)
	
#Stažení komponent
os.chdir(fdir+"/tmp")
if forge:
	down("forge.tar.gz",q,"Forge")
	down("libs.tar.gz",q,"knihovny")
down("servers.dat",q,"seznam serverů")
if core7:
	down("core172.tar.gz",q,"1.7.2 mody")
	core7dir=fdir+"/core172"
	if not os.path.isdir(core7dir):
		os.makedirs(core7dir)
if ic6:
	down("gt1710.tar.gz",q,"IC2 mody")
	ic6dir=fdir+"/ic1710"
	if not os.path.isdir(ic6dir):
		os.makedirs(ic6dir)

if apo:
	down("apoc1710.tar.gz",q,"Apocalypsu")
	apodir=fdir+"/apoc1710"
	if not os.path.isdir(apodir):
		os.makedirs(apodir)

if ic5:
	down("ic152.tar.gz",q,"IC2 mody pro 1.5.2")
	ic5dir=fdir+"/ic152"
	if not os.path.isdir(ic5dir):
		os.makedirs(ic5dir)
			
if eden:
	down("eden1710.tar.gz",q,"Eden mody")
	edendir=fdir+"/eden1710"
	if not os.path.isdir(edendir):
		os.makedirs(edendir)
		
if st:
	down("skytech1710.tar.gz",q,"Skytech mody")
	stdir=fdir+"/skytech1710"
	if not os.path.isdir(stdir):
		os.makedirs(stdir)
if core8:
	down("core18.tar.gz",q,"Core 1.8")
	core8dir=fdir+"/core18"
	if not os.path.isdir(core8dir):
		os.makedirs(core8dir)
#if op:
#	down("optifine164.tar.gz",q,"Optifine")
	
#if mmap=="r":
#	down("reismm164.tar.gz",q,"Rei's minimap")
	
#if mmap=="z":
#	down("zansmm164.tar.gz",q,"Zen's minimap")
	
#if mmap=="m":	
#	down("mapwritter164.tar.gz",q,"Map Writter")
#Instalace komponent
if forge:
	extract("forge.tar.gz",fdir+"/versions","Forge",False)
	extract("libs.tar.gz",fdir,"knihovny",False)
if ic6:
	if os.path.isdir(ic6dir+"/mods"):
		shutil.rmtree(ic6dir+"/mods")
	extract("gt1710.tar.gz",ic6dir,"IC2 mody",False)
	serinfo(ic6dir,ser)
if apo:
	if os.path.isdir(apodir+"/mods"):
		shutil.rmtree(apodir+"/mods")
	extract("apoc1710.tar.gz",apodir,"Apocalypsu",False)
	serinfo(apodir,ser)
if core7:
	if os.path.isdir(core7dir+"/mods"):
		shutil.rmtree(core7dir+"/mods")
	extract("core172.tar.gz",core7dir,"1.7.2 mody",False)
	serinfo(core7dir,ser)	
if eden:
	if os.path.isdir(edendir+"/mods"):
		shutil.rmtree(edendir+"/mods")
	extract("eden1710.tar.gz",edendir,"Eden mody",False)
	serinfo(edendir,ser)
if st:
	if os.path.isdir(stdir+"/mods"):
		shutil.rmtree(stdir+"/mods")
	extract("skytech1710.tar.gz",stdir,"Skytech mody",False)
	serinfo(stdir,ser)
if core8:
	if os.path.isdir(core8dir+"/mods"):
		shutil.rmtree(core8dir+"/mods")
	extract("core18.tar.gz",stdir,"Core 1.8 mody",False)
	serinfo(core8dir,ser)
if ic5:
	if os.path.isdir(ic5dir+"/mods"):
		shutil.rmtree(ic5dir+"/mods")
	extract("ic152.tar.gz",ic5dir,"IC2 1.5.2 mody",False)
	serinfo(ic5dir,ser)

#Profily
ic6f={u'gameDir': u''+ic6dir, u'name': u'IC2', u'lastVersionId': u'1.7.10-Forge10.13.2.1277'}
core7f={u'gameDir': u''+core7dir, u'name': u'BP-Core-1.7.2', u'lastVersionId': u'1.7.2-Forge10.12.1.1082'}
edenf={u'gameDir': u''+edendir, u'name': u'Eden', u'lastVersionId': u'1.7.10-Forge10.13.2.1277'}
ic5f={u'gameDir': u''+ic5dir, u'name': u'IC2 1.5.2', u'lastVersionId': u'1.5.2-Forge738'}
stf={u'gameDir': u''+stdir, u'name': u'SkyTech', u'lastVersionId': u'1.7.10-Forge10.13.2.1277'}
apoj={u'gameDir': u''+apodir, u'name': u'Apocalypsa', u'lastVersionId': u'1.7.10-Forge10.13.2.1277'}
core8f={u'gameDir': u''+core8dir, u'name': u'Core 1.8', u'lastVersionId': u'1.8-Forge11.14.1.1332'}
#úprava launcher_profiles.json
if jsonl:
    write("\nPřidávání profilů")
    os.chdir(fdir)
    try:
        with open("launcher_profiles.json") as json_file:
            data = json.load(json_file)
    except (ValueError) as e:
        print("Neplatný .json")
        end()		
    profiles=data["profiles"]
    if ic6:
        profiles["BP-IC-1.7.1.0"]=ic6f
    if core7:
        profiles["BP-Core-1.7.2"]=core7f	
    if eden:
        profiles["BP-Eden-1.7.1.0"]=edenf
    if ic5:
        profiles["BP-IC-1.5.2"]=ic5f
    if st:
        profiles["BP-SkyTech-1.7.10"]=stf
    if apo:
        profiles["BP-Apocalypse-1.7.10"]=apoj
    if core8:
        profiles["BP-Core-1.8"]=core8f
    with open('launcher_profiles.json', 'wb') as outfile:
        json.dump(data, outfile, sort_keys = True, indent = 4)
    print("...hotovo")    
#Generace nového .json
if cjson:
    os.chdir(fdir)
    write("\nGeneruji nový launcher_profiles.json")
    data={}
    profiles={}
    if ic6:
        profiles["BP-IC-1.7.1.0"]=ic6f
    if core7:		
        profiles["BP-Core-1.7.2"]=core7f
    if eden:
        profiles["BP-Eden-1.7.1.0"]=edenf
    if ic5:
        profiles["BP-IC-1.5.2"]=ic5f
    if st:
        profiles["BP-SkyTech-1.7.10"]=stf
    if apo:
        profiles["BP-Apocalypse-1.7.10"]=apoj
    if core8:
        profiles["BP-Core-1.8"]=core8f
    data["profiles"]=profiles	
    data["authenticationDatabase"]={}
    with open('launcher_profiles.json', 'wb') as outfile:
        json.dump(data, outfile, sort_keys = True, indent = 4)
    print("...hotovo")
#Poinstalační
write("\nOdstranuji dočasné soubory")
shutil.rmtree(fdir+"/tmp")
print("...hotovo")
print("\nInstalace kompletní")
end()


#   Copyright (C) 2014  SprtCZ

#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.	

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   http://www.gnu.org/licenses/gpl-3.0.html
								
