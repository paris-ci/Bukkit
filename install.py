#!/usr/bin/python
# -*- coding: UTF-8 -*-

## AUTO INSTALL PAR ARTHUR ##
print "[LOAD] Loading Vars"

############## VARS ##############

normal = "\033[0m"
# style
bold = "\033[1m"
underline = "\033[4m"
blink = "\033[5m"
reverse = "\033[7m"
concealed = "\033[8m"
# couleur texte
black = "\033[30m"
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
magenta = "\033[35m"
cyan = "\033[36m"
white ="\033[37m"
#couleurfond
on_black = "\033[40m"
on_red = "\033[41m"
on_green = "\033[42m"
on_yellow = "\033[43m"
on_blue = "\033[44m"
on_magenta = "\033[45m"
on_cyan = "\033[46m"
on_white = "\033[47m"



print "[LOAD] Importing libraries"

############# IMPORT #############


import datetime
import operator
import os
import re
import subprocess
import sys
import time
import urllib
import zipfile
# try :
# 	import pastebin
# except:
# 	print(red +  time.strftime("%H:%M:%S", time.gmtime()) + " [ERREUR] " + "PastebinAPI n'est pas installé ! Desactivation de pastebin" + normal)
# 	pastebinIntegre = False
# 	pass
# else:
# 	pastebinIntegre = True

print "[LOAD] Defining functions"
############## FUNC ##############

def printinfo(message): # Print formaté
	print(time.strftime("%H:%M:%S", time.gmtime()) + " [INFO] " + message) # Ici : heure + [INFO] et le message
	log.write(time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime()) + " [INFO] " + message + "\n") # Meme chose dans le log mais avec la date !
	
###############

def printwarn(message):
	print(yellow + time.strftime("%H:%M:%S", time.gmtime()) + " [ATTENTION] " + message + normal) # Cf printinfo() mais avec couleurs
	log.write(time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime()) + " [ATTENTION] " + message + "\n") # On enleve ls couleurs pour le log !
	
###############

def printerror(message):
	print(red +  time.strftime("%H:%M:%S", time.gmtime()) + " [ERREUR] " + message + normal) # Cf printinfo() et printwarn()
	log.write(time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime()) + " [ERREUR] " + message + "\n")
	
###############

def question(message):
	reponse = raw_input(green + time.strftime("%H:%M:%S", time.gmtime()) + " [QUES] " + message + normal) # Ici meme chose que printwarn() mais avec un raw_input
	log.write(time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime()) + " [QUEST] " + message + "\n")
	return reponse
	
############### MCLP : https://github.com/stevenleeg/Minecraft-Log-Parser

def mclp(path):
	sauvgarde = open("stats.txt","w") # Ouverture du fichier pour enregistrer les stats

	nbligne = 0 # Compteur de lignes
	actions = {
		"login": re.compile("([0-9]{4})\-([0-9]{2})\-([0-9]{2}) ([0-2][0-9])\:([0-9]{2})\:([0-9]{2}) \[INFO\] ([A-z0-9]*) ?\[\/[0-9.]{4,15}\:[0-9]*\]"),
	    "logout": re.compile("([0-9]{4})\-([0-9]{2})\-([0-9]{2}) ([0-2][0-9])\:([0-9]{2})\:([0-9]{2}) \[INFO\] ([A-z0-9]*) lost connection"),
	    "server_stop": re.compile("([0-9]{4})\-([0-9]{2})\-([0-9]{2}) ([0-2][0-9])\:([0-9]{2})\:([0-9]{2}) \[INFO\] Stopping server")
	}
	f = open(path)
	online = {}
	totals = {}
	for line in f.readlines():
		nbligne = nbligne + 1
		printinfo("Lecture de la ligne " + str(nbligne)) 
		regex = None
		action = None
		player = None
		time = None
		for action in actions:
			if actions[action].match(line):
				regex = actions[action]
				break
	
		if regex is not None:
			# Get the user's name and parse the datetime
			data = regex.split(line)
			player = data[7]
			time = datetime.datetime(int(data[1]), int(data[2]), int(data[3]), int(data[4]), int(data[5]), int(data[6]))
	
			# Now do things!
			if action is "login":
				online[player] = time
			elif action is "logout":
				if player not in totals:
					totals[player] = 0
				if player in online:
					delta = time - online[player]
				else:
					break

				totals[player] += delta.seconds
				del online[player]
			elif action is "server_stop":
				# Log off all players
				for player in online:
					if player not in totals:
						totals[player] = 0
					delta = time - online[player]
					totals[player] += delta.seconds
				online = {}
	printinfo("Calcul des temps ...")
	sort = sorted(totals.iteritems(), key=operator.itemgetter(1))
	times = []
	for player in sort:
		# Convert to hours/minutes/seconds
		time = "%20s: " % player[0]
		total = player[1]
		days = total / 86400
		if days > 0:
			time += "%2s days" % int(days)
			total -= int(days) * 86400
		else:
			time += "       "
		hours = total / 3600
		if hours > 0:
			time += " %2s hours" % int(hours)
			total -= int(hours) * 3600
		else:
			time += "         "
		mins = total / 60
		if mins > 0:
			time += " %2s minutes" % int(mins)
			total -= int(mins) * 60
		else:
			time += "           "
		if total > 0:
			time += " %2s seconds" % total
	
		times.append(time)

	times.reverse()
	sauvgarde.write("### Stats du serveur.log ### \n") # Mise en forme du fichier de sauvegarde
	sauvgarde.write("### " + str(nbligne) + " lignes lues ! ### \n")
	try :
		sauvgarde.write("### " + time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime()) + " ###")
	except: # En cas de probleme avec la date ...
		printerror("Petit probleme ...") 
		pass
	sauvgarde.write("\n\n\n")
	counter = 0
	for time in times:
		counter = counter + 1
		print "%2d) %s" % (counter, time)
		sauvgarde.write("%2d) %s" % (counter, time) + "\n")
	f.close()
	sauvgarde.close()

###############

def majCB():
	printinfo("Mise a jour du serveur !")
	ok = False
	try:
		printinfo("Supression de la precedante sauvegarde de craftbukkit")
		os.remove("./serveur/craftbukkit_OLD.jar")
	except:
		pass
	printinfo("Sauvegarde de l'ancien craftbukkit")
	os.rename("./serveur/craftbukkit.jar", "./serveur/craftbukkit_OLD.jar")
	try:
		dlbukkit("./serveur/")
	except:
		printerror("Dossier serveur introuvable : lance une installation !")
		installprocess() # Et ca se fait tout seul ! Génial non ?
###############

def generation(sleep,path= "./serveur/serveur/"):
	printinfo("Attente de la generation des fichiers")
	subprocess.call(["open", path +"/demarrer.command"]) # Lancement du serveur
	printinfo ("Patientez " + str(sleep) + " secondes ...")
	progressbar(sleep) # Barre de progression
	printinfo ("Arret du serveur")
	os.system ("killall java") # Quitter java
	printwarn ("Vous pouvez quitter le teminal <serveur> (celui avec [OPERATION TERMINEE] et sans couleurs)")
	
###############

def progressbar(longueur):
	toolbar_width = longueur

	# config de la barre
	sys.stdout.write("[%s]" % (" " * toolbar_width))
	sys.stdout.flush()
	sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

	for i in xrange(toolbar_width):
		time.sleep(1) # Attends 1 seconde
		# Ecriture sur la barre
		sys.stdout.write("~")
		sys.stdout.flush()
	sys.stdout.write("\n")

###############

def dl(nom,url):
	printinfo ("Installation de " + nom +" !")
	printwarn ("Cela peut prendre 1 a 2 minutes ... Veuillez patienter et ne pas aretter le processus")
	urllib.urlretrieve(url, './serveur/serveur/plugins/' + nom + ".jar") #DL + nom
	printinfo ("Téléchargement terminé")
	printinfo (nom + " installé")
	
###############

def dlzip(nom,url):
	printinfo ("Installation de " + nom + " !")
	printwarn ("Cela peut prendre 1 a 2 minutes ... Veuillez patienter et ne pas aretter le processus")
	urllib.urlretrieve(url, './serveur/serveur/plugins/' + nom + ".zip") # DL
	printinfo ("Téléchargement terminé")
	printinfo ("Extraction du .zip")
	with zipfile.ZipFile('./serveur/serveur/plugins/' + nom +'.zip', "r") as z: # Extraction des fichiers indispensables
	    z.extractall("./serveur/serveur/plugins/" + nom)
	printinfo (nom + " installé")
	printinfo ("Effacement de l'archive")
	os.system("rm ./serveur/serveur/plugins/" + nom + ".zip") # Suppression du zip
	printinfo ("Effacement terminé")
	printinfo ("Deplacement des plugins") 
	os.system("mv ./serveur/serveur/plugins/" + nom + "/* ./serveur/serveur/plugins") # Sortie du dossier décompressé
	printinfo ("""Suppression du dossier """ + nom + """ inutile""")
	os.system("rm -R ./serveur/serveur/plugins/" + nom) # Suppression du dossier décompressé vide
	
###############
	
def createpath(path):
	if not os.path.isdir(path):
		os.mkdir(path)
		
###############

def install():
	printinfo ("Instalation automatique de bukkit sous mac" )
	createpath("./serveur")
	createpath("./serveur/serveur")
	command = open("./serveur/serveur/demarrer.command","w")
	printinfo ("Creation du script de demarrage !")
	command.write("""#!/bin/bash \n cd "$( dirname "$0" )"\njava -server -Xmx2G -jar ./craftbukkit.jar\n """)
	os.system("chmod +x ./serveur/serveur/demarrer.command")
	command.close()
	dlbukkit("./serveur/serveur/")
	printinfo ("Lancement du serveur ... Veuillez ne rien toucher !")
	generation(60) # Generation des fichiers par un lancement du serveur

###############

def dlbukkit(path):
	ok = False
	while ok is not True:
		version = question("Quelle version de craft bukkit voulez vous ? \n * Les dernieres versions : \n \t * Build de devloppement (dev) \n \t * Build beta (beta) \n \t * Build recomandée (recomandee) \n * Les versions precises \n \t * 1.6.2\n \t * 1.6.1 \n \t * 1.5.2 \n \t * 1.5.1\n \t * 1.5\n \t * 1.4.7\n \t * 1.4.6\n \t * 1.4.5\n \t * 1.4.4\n \t * 1.4.2\n \t * 1.3.2\n \t * 1.3.1\n \t * 1.2.5\n \t * 1.2.4\n \t * 1.2.3\n \t * 1.2.1 \n \t * 1.1 \n \t * 1.0.1 \n \t * 1.0.0 \n \t * B1.8.1 \n \t * B0.0.1 \n>>>" )
		if version == "recommandee":
			printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
			printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
			urllib.urlretrieve('http://dl.bukkit.org/latest-rb/craftbukkit.jar', path + '/craftbukkit.jar') # téléchargement de CB (latest - RB)
			ok = True
		elif version == "beta":
			printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
			printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
			urllib.urlretrieve('http://dl.bukkit.org/latest-beta/craftbukkit-beta.jar', path + 'craftbukkit.jar') # téléchargement de CB (latest - beta)
			ok = True
		elif version == "dev":
			printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
			printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
			urllib.urlretrieve('http://dl.bukkit.org/latest-dev/craftbukkit-dev.jar', path + 'craftbukkit.jar') # téléchargement de CB (latest - dev)
			ok = True
		elif version == "1.6.2":
			printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
			printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
			urllib.urlretrieve('http://dl.bukkit.org/downloads/craftbukkit/get/02213_1.6.2-R0.1/craftbukkit-dev.jar', path + 'craftbukkit.jar') 
			ok = True
		elif version == "1.6.1":
			printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
			printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
			urllib.urlretrieve('http://dl.bukkit.org/downloads/craftbukkit/get/02194_1.6.1-R0.1/craftbukkit-dev.jar', path + 'craftbukkit.jar') 
			ok = True
		elif version == "1.5.2":
			printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
			printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
			urllib.urlretrieve('http://dl.bukkit.org/downloads/craftbukkit/get/02180_1.5.2-R1.1/craftbukkit-dev.jar', path + 'craftbukkit.jar') 
			ok = True
		elif version == "1.5.1":
			printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
			printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
			urllib.urlretrieve('http://dl.bukkit.org/downloads/craftbukkit/get/02099_1.5.1-R0.3/craftbukkit-dev.jar', path + 'craftbukkit.jar') 
			ok = True
		elif version == "1.5":
			printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
			printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
			urllib.urlretrieve('http://dl.bukkit.org/downloads/craftbukkit/get/01980_1.5-R0.1/craftbukkit-dev.jar', path + 'craftbukkit.jar') 
			ok = True
		elif version == "1.4.7":
			printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
			printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
			urllib.urlretrieve('http://dl.bukkit.org/downloads/craftbukkit/get/01910_1.4.7-R1.1/craftbukkit-dev.jar', path + 'craftbukkit.jar') 
			ok = True
		elif version == "1.4.6":
			printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
			printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
			urllib.urlretrieve('http://dl.bukkit.org/downloads/craftbukkit/get/01800_1.4.6-R0.4/craftbukkit-dev.jar', path + 'craftbukkit.jar') 
			ok = True
		elif version == "1.4.5":
			printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
			printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
			urllib.urlretrieve('http://dl.bukkit.org/downloads/craftbukkit/get/01707_1.4.5-R1.0/craftbukkit.jar', path + 'craftbukkit.jar') 
			ok = True
		elif version == "1.4.4":
			printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
			printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
			urllib.urlretrieve('http://dl.bukkit.org/downloads/craftbukkit/get/01571_1.4.4-R0.1/craftbukkit-dev.jar', path + 'craftbukkit.jar') 
			ok = True
		elif version == "1.4.2":
			printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
			printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
			urllib.urlretrieve('http://dl.bukkit.org/downloads/craftbukkit/get/01554_1.4.2-R0.3/craftbukkit-dev.jar', path + 'craftbukkit.jar') 
			ok = True
		elif version == "1.3.2":
			printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
			printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
			urllib.urlretrieve('http://dl.bukkit.org/downloads/craftbukkit/get/01479_1.3.2-R3.0/craftbukkit.jar', path + 'craftbukkit.jar') 
			ok = True
		elif version == "1.3.1":
			printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
			printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
			urllib.urlretrieve('http://dl.bukkit.org/downloads/craftbukkit/get/01389_1.3.1-R2.1/craftbukkit-dev.jar', path + 'craftbukkit.jar') 
			ok = True
		elif version == "1.2.5":
			printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
			printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
			urllib.urlretrieve('http://dl.bukkit.org/downloads/craftbukkit/get/01260_1.2.5-R5.1/craftbukkit-dev.jar', path + 'craftbukkit.jar') 
			ok = True
		elif version == "1.2.4":
			printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
			printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
			urllib.urlretrieve('http://dl.bukkit.org/downloads/craftbukkit/get/00993_1.2.4-R1.0/craftbukkit.jar', path + 'craftbukkit.jar') 
			ok = True
		elif version == "1.2.3":
			printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
			printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
			urllib.urlretrieve('http://dl.bukkit.org/downloads/craftbukkit/get/00954_1.2.3-R0.3/craftbukkit-dev.jar', path + 'craftbukkit.jar') 
			ok = True
		elif version == "1.2.2":
			printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
			printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
			urllib.urlretrieve('http://dl.bukkit.org/downloads/craftbukkit/get/00823_1.2.2-R0.1/craftbukkit-dev.jar', path + 'craftbukkit.jar') 
			ok = True
		elif version == "1.1":
			printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
			printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
			urllib.urlretrieve('http://dl.bukkit.org/downloads/craftbukkit/get/00790_1.1-R6/craftbukkit.jar', path + 'craftbukkit.jar') 
			ok = True
		elif version == "1.0.1":
			printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
			printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
			urllib.urlretrieve('http://dl.bukkit.org/downloads/craftbukkit/get/00364_1.0.1-R2/craftbukkit-dev.jar', path + 'craftbukkit.jar') 
			ok = True
		elif version == "1.3.2":
			printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
			printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
			urllib.urlretrieve('http://dl.bukkit.org/downloads/craftbukkit/get/01479_1.3.2-R3.0/craftbukkit.jar', path + 'craftbukkit.jar') 
			ok = True
		elif version == "1.0.0":
			printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
			printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
			urllib.urlretrieve('http://dl.bukkit.org/downloads/craftbukkit/get/00251_1.0.0/craftbukkit-dev.jar', path + 'craftbukkit.jar') 
			ok = True
		elif version == "B1.8.1":
			printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
			printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
			urllib.urlretrieve('http://dl.bukkit.org/downloads/craftbukkit/get/00128_1.8.1-R5/craftbukkit-dev.jar', path + 'craftbukkit.jar') 
			ok = True
		elif version == "B0.0.1":
			printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
			printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
			urllib.urlretrieve('http://dl.bukkit.org/downloads/craftbukkit/get/00042_0.0.1/craftbukkit-dev.jar', path + 'craftbukkit.jar') 
			ok = True
		elif version =="pass":
			ok = True
			printwarn ("Aucun telechargement !!!!")
		else :
			printerror("Version " + version + " non trouvée ... Choisisez entre les choix proposés")


###############

def plugins(lancer):
	## INSTALL ESSENTIALS ##
	installer = "oui"
	continuer = False
	while continuer is False :
		installer = question("Installer essentials ? oui/non >>>")
		if installer == "oui" or installer == "non":
			continuer = True
		else:
			printerror("Oui ou non !")

	if installer == "oui":
		dlzip ("essentials","http://ess.ementalo.com/repository/download/bt2/.lastSuccessful/Essentials.zip?guest=1")
		if lancer == True:
			printinfo ("Lancement du serveur pour creer la config essentials !")
			generation(40)

	installer = "oui"
	continuer = False
	while continuer is False :
		installer = question("Installer PermissionsEx ? oui/non >>>")
		if installer == "oui" or installer == "non":
			continuer = True
		else:
			printerror("Oui ou non !")
	if installer == "oui":
		## INSTALL PEX ##
		dlzip("pex","http://dev.bukkit.org/media/files/659/820/PermissionsEx-1.19.5-package.zip")

	installer = "oui"
	continuer = False
	while continuer is False :
		installer = question("Installer WorldEdit ? oui/non >>>")
		if installer == "oui" or installer == "non":
			continuer = True
		else:
			printerror("Oui ou non !")
	if installer == "oui":
		## INSTALL WE ##
		dlzip("we","http://dev.bukkit.org/media/files/698/942/worldedit-5.5.6.zip")

	installer = "oui"
	continuer = False
	while continuer is False :
		installer = question("Installer WorldGuard ? oui/non >>>")
		if installer == "oui" or installer == "non":
			continuer = True
		else:
			printerror("Oui ou non !")
	if installer == "oui":
		## INSTALL WG ##
		dlzip("wg","http://dev.bukkit.org/media/files/702/797/worldguard-5.7.4.zip")
	installer = "oui"
	continuer = False
	while continuer is False :
		installer = question("Installer BoseEconomy ? oui/non >>>")
		if installer == "oui" or installer == "non":
			continuer = True
		else:
			printerror("Oui ou non !")
	if installer == "oui":	
		## INSTALL BOSE ECO ##
		dlzip("boseecon","http://dev.bukkit.org/media/files/577/409/BOSEcon0731.zip")
	installer = "oui"
	continuer = False
	while continuer is False :
		installer = question("Installer DynMap ? oui/non >>>")
		if installer == "oui" or installer == "non":
			continuer = True
		else:
			printerror("Oui ou non !")
	if installer == "oui":
		## INSTALL DYNMAP ##
		dlzip("dynmap","http://webbukkit.org/jenkins/public/dynmap/dynmap-HEAD-bin.zip")
		os.system("rm ./serveur/serveur/plugins/wg/contrib") # Dossier particulier 
		installer = "oui"
	continuer = False
	while continuer is False :
		installer = question("Installer Vault ? oui/non >>>")
		if installer == "oui" or installer == "non":
			continuer = True
		else:
			printerror("Oui ou non !")
	if installer == "oui":
		## INSTALL VAULT ##
		dl("vault","http://dev.bukkit.org/media/files/694/78/Vault.jar") 
	installer = "oui"
	continuer = False
	while continuer is False :
		installer = question("Installer NoCheatPlus ? oui/non >>>")
		if installer == "oui" or installer == "non":
			continuer = True
		else:
			printerror("Oui ou non !")
	if installer == "oui":
		## INSTALL NO CHEAT PLUS ##
		dl("ncp","http://ci.md-5.net/job/NoCheatPlus/lastSuccessfulBuild/artifact/target/NoCheatPlus.jar")

###############

def config():
	printinfo ("Genération des dernieres configurations")
	generation(30)
	op = question("Entrez le nom de l'operateur du serveur >>>")
	sauvgarde = open("./serveur/serveur/ops.txt","a")
	sauvgarde.write(str(op) + "\n")
	sauvgarde.close()
	printinfo ("Operateur ajouté a la liste des operateurs...")
	sauvgarde = open("./serveur/serveur/white-list.txt","a")
	sauvgarde.write(str(op) + "\n")
	sauvgarde.close()
	printinfo ("Operateur ajouté a la whitelist")
	proprietees = open("./serveur/serveur/server.properties","r")
	temp = open("./serveur/serveur/.server.properties.temp","a")
	for ligne in proprietees: # Ici on touche au serveur.properties
		if ligne == "allow-nether=true\n":
			prop("Les joueurs doivent t'ils acceder au nether ? (oui/non) >>>","allow-nether=true","allow-nether=false","allow-nether=true")
		elif ligne == "allow-flight=false\n":
			prop("Les joueurs peuvent t'ils voler ? (oui/non) >>>","allow-flight=true","allow-flight=false","allow-flight=false")
		elif ligne == "hardcore=false\n":
			prop("Activer le mode hardcore? (oui/non) >>>","hardcore=true","hardcore=false","hardcore=false")
		elif ligne == "online-mode=true\n":
			prop("Accepter les versions crakées ? (oui/non) >>>","online-mode=true","online-mode=false","online-mode=true")
		elif ligne == "pvp=true\n":
			prop("Autoriser le PvP ? (oui/non) >>>","pvp=true","pvp=false","pvp=true")
		elif ligne == "max-players=20\n":
			slots = question("Indiquez le nombre de slots >>>")
			temp.write("max-players=" + slots)
		elif "motd=" in ligne:
			motd = question("Indiquez le motd >>>")
			temp.write("motd=" + motd)
		else: # Ligne(s) qui ne correspond a rien = retranscrites a l'identique !
			temp.write(ligne + "\n")
	os.system("rm ./serveur/serveur/server.properties")
	os.rename("./serveur/serveur/.server.properties.temp", "./serveur/serveur/server.properties")
	
###############

def finition():
	printinfo ("Génération des derniers fichiers !")
	os.system("rm -R ./serveur/serveur/plugins/Modifyworld.jar") # Plugin restricteur tres embettant ...
	generation(60)
	printinfo ("Deplacement des fichiers serveurs ...")
	os.system("mv ./serveur/serveur/* ./serveur")
	printinfo ("Supression du dossier temporaire")
	os.system("rm -R ./serveur/serveur")
	printinfo ("Suppression des readme")
	os.system("rm -R ./serveur/plugins/CHANGELOG.txt")
	os.system("rm -R ./serveur/plugins/LICENSE.txt")
	os.system("rm -R ./serveur/plugins/README.html")
	temps = float(time.time()) - float(chrono)
	tempsmin = float(temps)/float(60)
	printinfo ("Temps passé sur l'install : " + str(temps) + " secondes soit " + str(tempsmin) + " minute(s)") # Fin du chrono
	
	
###############

def prop(question_,oui,non,defaut): # Fonction de mise a jour du server.properties
	temp = open("./serveur/serveur/.server.properties.temp","a")
	reponse = question(question_) # Attention a ne pas confondre avec la fonction !!
	if reponse == "non":
		temp.write(non + "\n")
	elif reponse == "oui":
		temp.write(oui + "\n")
	else :
		printerror("Entree non comprise : valeur par defaut")
		temp.write(defaut+ "\n")
	
###############

def installprocess():
	install()
	printinfo ("Passons a l'installation des plugins ...")
	plugins(True)
	printinfo ("Passons a la configuration")
	config()
	printinfo ("Passons a la finition...")
	finition()
	printinfo ("FIN DE L'INSTALATION !")
	print("\t **                    **              **  **             **   **                     **********                            **                    **\n\t/**                   /**             /** /**            /**  //                     /////**///                            //                    /**\n\t/** *******   ****** ******  ******   /** /**  ******   ****** **  ******  *******       /**      *****  ****** **********  ** *******   *****   /**\n\t/**//**///** **//// ///**/  //////**  /** /** //////** ///**/ /** **////**//**///**      /**     **///**//**//*//**//**//**/**//**///** **///**  /**\n\t/** /**  /**//*****   /**    *******  /** /**  *******   /**  /**/**   /** /**  /**      /**    /******* /** /  /** /** /**/** /**  /**/*******  /**\n\t/** /**  /** /////**  /**   **////**  /** /** **////**   /**  /**/**   /** /**  /**      /**    /**////  /**    /** /** /**/** /**  /**/**////   // \n\t/** ***  /** ******   //** //******** *** ***//********  //** /**//******  ***  /**      /**    //******/***    *** /** /**/** ***  /**//******   **\n\t// ///   // //////     //   //////// /// ///  ////////    //  //  //////  ///   //       //      ////// ///    ///  //  // // ///   //  //////   //\n ")
	
###############

def majPL():
	try:
		os.mkdir("./serveur/serveur") # Creation des dossiers temporaires
		os.mkdir("./serveur/serveur/plugins")
	except:
		printerror("Hummm ... Les dossiers sont deja crées ?")
		pass
	plugins(False)
	os.system("mv ./serveur/serveur/plugins/@ ./serveur/plugins")
	finition()
	
###############

def tbg(path):
	leaderboard = open(path,"r") #Ouverture du fichier
	joueurs = []
	for ligne in leaderboard:
	
		joueurs.append(ligne.replace("\n","")) # Ficher dans une liste
	
	joueurs.sort() # Tout est bien rangé !
	joueurprecedent = ""
	for joueur in joueurs:
		if not joueurprecedent == joueur :
			printinfo(str(joueur) + " a gagné " + str(joueurs.count(joueur)) + " fois")
		joueurprecedent = joueur
		
###############

def maintenance():
	printinfo("Suppression des logs")
	os.system("rm log.txt")
	printinfo("Supression du dossier temporaire")
	os.system("rm ./serveur/serveur")

###############

def devmenu():
	printwarn("Vous etes maintenent dans le devmenu ! Faites attention ici !")
	choix = question("Que faire ? \n *Afficher le log \t\t\t(log) \n *Afficher les erreurs du log \t\t(elog) \n *Afficher une erreur \t\t\t(erreur) \n *Afficher l'adresse du github \t\t(github)\n *Lancer le serveur \t\t\t(lancer) \n>>>")

	if choix == "log"or choix == "lo":
		logr = open("./log.txt","r") # Creation - ouverture du fichier de log
		numligne = 0
		for ligne in logr:
			numligne = numligne + 1
			print(str(numligne) + ") " + ligne)
		logr.close
	elif choix == "elog" or choix == "el":
		logr = open("./log.txt","r") # Creation - ouverture du fichier de log
		numligne = 0
		for ligne in logr:
			numligne = numligne + 1
			if "[ERREUR]" in ligne:
				print(str(numligne) + ") " + ligne)
		logr.close
	elif choix == "erreur" or choix == "er":
		message = question("Quel message d'erreur ? >>>")
		raise NameError(message)
	elif choix == "github" or choix == "g":
		printinfo("Adresse du github : https://github.com/paris-ci/Bukkit")
	elif choix == "lancer" or choix == "la":
		sec = question("Combien de secondes de generation ? >>>")
		generation(int(sec),"./serveur")
	else:
		printerror("Je n'ai pas compris votre choix ! Retour au menu !")

###############

def menu():	# Menu un peu moche ...
	ok = False
	while ok is not True:
		chrono = time.time()
		choix = question("Bukkit (bukkit) ou autres (autres) ou quitter (q)? >>>")
		if choix == "bukkit" or choix == "b":
			choix = question("Instalation (install), ou mise a jour (maj) ? >>>")
			if choix == "install" or choix == "i":
				installprocess()
			elif choix == "maj" or choix == "m":
				choix = question("Mise a jour de craft bukkit (cb) ou des plugins (pl) ? >>>")
				if choix == "pl" or choix == "p":
					majPL()
				elif choix == "cb" or choix == "c":
					majCB()
				else:
					printerror("Je n'ai pas compris votre choix ! Retour au menu !")
			else:
				printerror("Je n'ai pas compris votre choix ! Retour au menu !")
		elif choix == "autres" or choix == "a":
			choix = question("Statistiques (stats) ou configuration de craftbukkit (config) ou maintenance (maintenance) ? >>>")
			if choix == "stats" or choix == "s":
				choix = question("Analyse du log (log) ou du leaderboard de The BukkitGames (tbg) ? >>>")
				if choix == "log" or choix == "l":
					# try:
					# 	mclp("./serveur/server.log")
					# except:
					# 	path = question("Deplacez ici votre fichier server.log et tapez entrer >>>")
					# 	printinfo ("Lancement du processus")
					choix = question("Analyse du log simple (slog) ou analyse du log continue(clog) ? >>>")
					path = question("Deplacez ici votre fichier server.log et tapez entrer >>>")
					if choix == "slog" or choix == "s":
						mclp(path.replace(" ",""))
					elif choix == "clog" or "c":
						continuer = True
						
						while continuer is not False:
							try:
								temps = question("Combien de secondes entre chaque relancement ? (60 sec = 1 minute) >>>")
								int(temps)
							except:
								printerror("Entre un nombre ici !")
							else : 
								continuer = False
						continuer = True
						while continuer is not False:
							try :
								mclp(path.replace(" ",""))
								printinfo("Attente de 60 secondes avant de re-lancer le script -- Pour le quitter, appuyez sur ctrl et c en meme temps !")
								progressbar(60)
							except KeyboardInterrupt:
								print("")
								printwarn("Arret du script ? -- KILLED")
								continuer = False
								pass

					else:
						printerror("Je n'ai pas compris votre choix ! Retour au menu !")
				elif choix == "tbg" or choix == "t":
					# try:
					# 	tbg("./serveur/plugins/thebukkitgames/leaderboard.yml")
					# except:
					# 	path = question("Deplacez ici votre fichier leaderboard et tapez entrer >>>")
					# 	printinfo ("Lancement du processus")
					# 	tbg(path.replace(" ",""))
					path = question("Deplacez ici votre fichier leaderboard et tapez entrer >>>")
					printinfo ("Lancement du processus")
					tbg(path.replace(" ",""))
				else:
					printerror("Je n'ai pas compris votre choix ! Retour au menu !")

			elif choix == "config" or choix == "c":
				config()
			elif choix == "maintenance" or choix == "m":
				maintenance()
			else:
				printerror("Je n'ai pas compris votre choix ! Retour au menu !")
		elif choix == "q":
			ok = True
		elif choix == "dev" or choix == "d":
			devmenu()	
		else:
			printerror("Je n'ai pas compris votre choix !")


############## MAIN ##############

#       #      #      #########  ##    #
##     ##     # #         #      # #   #
# #   # #    #   #        #      #  #  #
#  # #  #   #######       #      #   # #
#   #   #  #       #  #########  #    ##


try:
	log = open("./log.txt","a") # Creation - ouverture du fichier de log
	printinfo("[LOAD] Starting main ...")

	print("\t @@@@@@   @@                                                              @@\n\t/@////@@ //                                                              /@@\n\t/@   /@@  @@  @@@@@  @@@@@@@  @@    @@  @@@@@  @@@@@@@  @@   @@  @@@@@   /@@\n\t/@@@@@@  /@@ @@///@@//@@///@@/@@   /@@ @@///@@//@@///@@/@@  /@@ @@///@@  /@@\n\t/@//// @@/@@/@@@@@@@ /@@  /@@//@@ /@@ /@@@@@@@ /@@  /@@/@@  /@@/@@@@@@@  /@@\n\t/@    /@@/@@/@@////  /@@  /@@ //@@@@  /@@////  /@@  /@@/@@  /@@/@@////   // \n\t/@@@@@@@ /@@//@@@@@@ @@@  /@@  //@@   //@@@@@@ @@@  /@@//@@@@@@//@@@@@@   @@\n\t///////  //  ////// ///   //    //     ////// ///   //  //////  //////   // \n")
	printwarn("Bon serveur pvp : pvp.api-d.com")
	printwarn("Bon serveur HG : hg.api-d.com:25566")
	chrono = time.time()
	menu()


	log.close() # Au revoir les logs !
except KeyboardInterrupt:
	print("")
	printerror("Arret forcé du script ? -- KILLED")
	sys.exit()
except:
	print("")
	printerror("Une erreur est survenue ... Le script s'arette !")
	raise
else :
	print(time.strftime("%H:%M:%S", time.gmtime()) + " [INFO] " + "Au revoir !")
finally:
	print(time.strftime("%H:%M:%S", time.gmtime()) + " [INFO] " + "Vous quittez le script !")
	progressbar(2)
	log.close() # Au revoir les logs !


############################################################

######  ######  ####### 
#       #    #  #       
######  #    #  ####    
#       #    #  #       
######  ######  #       

# Enfin !
