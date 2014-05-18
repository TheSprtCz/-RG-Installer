#!/usr/bin/python
# -*- coding: utf-8 -*-

#Načtění komponent Pythonu
import os
import time
import urllib2
import urllib
import json
import sys
import termios
import fcntl
import tarfile
import shutil
import subprocess

#Přípravy
os.system('setterm -cursor off')
version="1.2b"

#Defaultni hodnoty
ic6=True
ic5=False
eden=True
st=True
forge=True
op=True
mmap="r"
ser=True
q=False
urlm="http://www.mirc.cz/"
cure7=True

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
	print "Stahuji: %s Velikost: %s B" % (file_name, file_size)
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
   		print status,
	f.close()
def downloadq(url,text):
	write("Stahuji "+text)
	name = url.split('/')[-1]
	urllib.urlretrieve (url, name)
	print "...hotovo"
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
	print "Pro ukončení stiskněte libovolnou klávesu"
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
		print ""
		return True
	else:
		if q==True:
			write("...nevybráno")
		print ""	
		return False
def extract(name,path,text,quiet):
	if not quiet:
		write("Instaluji "+text)
	file=tarfile.open(name)
	file.extractall(path)
	file.close
	if not quiet:
		print "..hotovo"
def serinfo(path,ser):
	if ser:
		shutil.copy2("servers.dat",path)
	else:
		if not os.path.exists(path+"/servers.dat"):
			shutil.copy2("servers.dat",path)
			#print "Kopiruji seznam serveru"
#Kontrola verze
if not sys.version_info[:1] == (2,):
	print "Chyba: Je potřebná verze 2.x pythonu"
	end()
											
#Přeinstalační přípravy
print "Vítejte v Instalátoru B-paradise, vytvořeného uživatelem Sprt ("+version+")"
fdir=raw_input("\nVlozte cilovou slozku: ")
if not fdir[0]=="/":
	fdir=os.getcwd()+"/"+fdir
if not os.path.isdir(fdir):
	print "Slozka "+fdir+" neexistuje, chcete ji vytvořit? A/N "
	bool=read(1)
	if bool=="a" or bool=="A":
		write("Vytvářím složku "+fdir)
		os.makedirs(fdir)
		print "...hotovo"
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
	print "\nVaše java("+java_v+") je zastaralá a proto Modpacky B-Paradise nemusí fungovat správně"
	print "Prosím aktualizujte svoji javu na verzi 1.7 na www.java.com"
	
#Kontrola launcheru
if not os.path.exists(fdir+"/launcher_profiles.json"):
	jsonl=False
	cjson=select("\nNebyl nalezen soubor s profily(launcher_profiles.json), chcete ho vytvořit?",True)	
else:
	jsonl=True
	cjson=False
	
#Výběr komponent
sel=select("\nChcete použít k instalaci standardní nastavení? (Všechny modpacky, OptiFine, Rei's minimap)",True)
if not sel:
	ic6=select("Chcete nainstalovat IC2 mody?",True)
	ic5=select("Chcete nainstalovat IC2 mody na 1.5.2?",True)
	eden=select("Chcete nainstalovat Eden mody?",True)
	st=select("Chcete nainstalovat SkyTech mody?",True)
	op=select("Chcete nainstalovat Optifine?",True)
	core7=select("Chcete nainstalovat 1.7.2 mody?",True)
	print "Jaky z minimap modu chcete nainstalovat?"
	write("R-Rei's minimap, Z-Zan's minimap, M-MapWriter, N-Žádný ")
	let=getch()
	if let=="r" or let=="R":
		write("...Rei's minimap")
		mmap="r"
	if let=="z" or let=="Z":
		write("...Zan's minimap")
		mmap="z"
	if let=="m" or let=="M":
		write("...MapWritter")
		mmap="m"
	if let=="n" or let=="N":
		write("...Žádný")
		mmap="n"
	print ""
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
	down("ic164.tar.gz",q,"IC2 mody")
	ic6dir=fdir+"/ic164"
	if not os.path.isdir(ic6dir):
		os.makedirs(ic6dir)

if ic5:
	down("ic152.tar.gz",q,"IC2 mody pro 1.5.2")
	ic5dir=fdir+"/ic152"
	if not os.path.isdir(ic5dir):
		os.makedirs(ic5dir)
			
if eden:
	down("eden164.tar.gz",q,"Eden mody")
	edendir=fdir+"/eden164"
	if not os.path.isdir(edendir):
		os.makedirs(edendir)
		
if st:
	down("iconly164.tar.gz",q,"Skytech mody")
	stdir=fdir+"/iconly164"
	if not os.path.isdir(stdir):
		os.makedirs(stdir)
		
if op:
	down("optifine164.tar.gz",q,"Optifine")
	
if mmap=="r":
	down("reismm164.tar.gz",q,"Rei's minimap")
	
if mmap=="z":
	down("zansmm164.tar.gz",q,"Zen's minimap")
	
if mmap=="m":	
	down("mapwritter164.tar.gz",q,"Map Writter")
#Instalace komponent
if forge:
	extract("forge.tar.gz",fdir+"/versions","Forge",False)
	extract("libs.tar.gz",fdir,"knihovny",False)
if ic6:
	if os.path.isdir(ic6dir+"/mods"):
		shutil.rmtree(ic6dir+"/mods")
	extract("ic164.tar.gz",ic6dir,"IC2 mody",False)
	serinfo(ic6dir,ser)
	minmap(ic6dir,mmap)
	if op:
		extract("optifine164.tar.gz",ic6dir+"/mods","text",True)
if core7:
	if os.path.isdir(core7dir+"/mods"):
		shutil.rmtree(core7dir+"/mods")
	extract("ic164.tar.gz",core7dir,"1.7.2 mody",False)
	serinfo(core7dir,ser)	
if eden:
	if os.path.isdir(edendir+"/mods"):
		shutil.rmtree(edendir+"/mods")
	extract("eden164.tar.gz",edendir,"Eden mody",False)
	serinfo(edendir,ser)
	minmap(edendir,mmap)
	if op:
		extract("optifine164.tar.gz",edendir+"/mods","text",True)				
if st:
	if os.path.isdir(stdir+"/mods"):
		shutil.rmtree(stdir+"/mods")
	extract("iconly164.tar.gz",stdir,"Skytech mody",False)
	serinfo(stdir,ser)
	minmap(stdir,mmap)
	if op:
		extract("optifine164.tar.gz",stdir+"/mods","text",True)	
if ic5:
	if os.path.isdir(ic5dir+"/mods"):
		shutil.rmtree(ic5dir+"/mods")
	extract("ic164.tar.gz",ic5dir,"IC2 mody",False)
	serinfo(ic5dir,ser)
	minmap(ic5dir,mmap)	
	if op:
		extract("optifine164.tar.gz",ic5dir+"/mods","text",True)

#úprava launcher_profiles.json
if jsonl:
	write("\nPřidávání profilů")
	os.chdir(fdir)
	try:
		with open("launcher_profiles.json") as json_file:
    			data = json.load(json_file)
    	except ValueError:
    		print("Neplatný .json")
    		end()		
	profiles=data["profiles"]
	if ic6:
		ic6f={u'gameDir': u''+ic6dir, u'name': u'IC2', u'lastVersionId': u'1.6.4-Forge9.11.1.953'}
		profiles["BP-IC-1.6.4"]=ic6f
	if core7:
		core7f={u'gameDir': u''+core7dir, u'name': u'BP-Core-1.7.2', u'lastVersionId': u'1.7.2-Forge10.12.1.1082'}
		profiles["BP-Core-1.7.2"]=core7f	
	if eden:
		edenf={u'gameDir': u''+edendir, u'name': u'Eden', u'lastVersionId': u'1.6.4-Forge9.11.1.953'}
		profiles["BP-Eden-1.6.4"]=edenf
	if ic5:
		ic5f={u'gameDir': u''+ic5dir, u'name': u'IC2 1.5.2', u'lastVersionId': u'1.5.2-Forge738'}
		profiles["BP-IC-1.5.2"]=ic5f
	if st:
		stf={u'gameDir': u''+stdir, u'name': u'SkyTech', u'lastVersionId': u'1.6.4-Forge9.11.1.953'}
		profiles["BP-SkyTech-1.6.4"]=stf	
	with open('launcher_profiles.json', 'wb') as outfile:
  		json.dump(data, outfile, sort_keys = True, indent = 4)
  	print "...hotovo"
  	
#Generace nového .json
if cjson:
	os.chdir(fdir)
	write("\nGeneruji nový launcher_profiles.json")
	data={}
	profiles={}
	if ic6:
		ic6f={u'gameDir': u''+ic6dir, u'name': u'IC2', u'lastVersionId': u'1.6.4-Forge9.11.1.953'}
		profiles["BP-IC-1.6.4""]=ic6f
	if core7:
		core7f={u'gameDir': u''+core7dir, u'name': u'BP-Core-1.7.2', u'lastVersionId': u'1.7.2-Forge10.12.1.1082'}
		profiles["BP-Core-1.7.2"]=core7f
	if eden:
		edenf={u'gameDir': u''+edendir, u'name': u'Eden', u'lastVersionId': u'1.6.4-Forge9.11.1.953'}
		profiles["BP-Eden-1.6.4"]=edenf
	if ic5:
		ic5f={u'gameDir': u''+ic5dir, u'name': u'IC2 1.5.2', u'lastVersionId': u'1.5.2-Forge738'}
		profiles["BP-IC-1.5.2"]=ic5f
	if st:
		stf={u'gameDir': u''+stdir, u'name': u'SkyTech', u'lastVersionId': u'1.6.4-Forge9.11.1.953'}
		profiles["BP-SkyTech-1.6.4"]=stf
	data["profiles"]=profiles	
	data["authenticationDatabase"]={}
	with open('launcher_profiles.json', 'wb') as outfile:
  		json.dump(data, outfile, sort_keys = True, indent = 4)
  	print("...hotovo")					
#Poinstalační
write("\nOdstranuji dočasné soubory")
shutil.rmtree(fdir+"/tmp")
print "...hotovo"
print "\nInstalace kompletní"
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
								
