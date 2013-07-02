#!/usr/bin/python
# -*- coding: UTF-8 -*-

## AUTO INSTALL PAR ARTHUR ##

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



import sys
import os
import zipfile
import urllib
import time
import subprocess
import re
import datetime
import operator




############## FUNC ##############

def printinfo(message):
	print(time.strftime("%H:%M:%S", time.gmtime()) + " [INFO] " + message)
	log.write(time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime()) + " [INFO] " + message + "\n")
###############

def printwarn(message):
	print(yellow + time.strftime("%H:%M:%S", time.gmtime()) + " [ATTENTION] " + message + normal)
	log.write(time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime()) + " [ATTENTION] " + message + "\n")
###############

def printerror(message):
	print(red +  time.strftime("%H:%M:%S", time.gmtime()) + " [ERREUR] " + message + normal)
	log.write(time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime()) + " [ERREUR] " + message + "\n")
############### MCLP : https://github.com/stevenleeg/Minecraft-Log-Parser

def mclp(path):
	sauvgarde = open("stats.txt","w")
	nbligne = 0
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
	sauvgarde.write("### Stats du serveur.log ### \n")
	sauvgarde.write("### " + str(nbligne) + " lignes lues ! ### \n")
	try :
		sauvgarde.write("### " + time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime()) + " ###")
	except:
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
		while ok is not True:
			version = raw_input("Quelle version de craft bukkit voulez vous ? Une build de '" + cyan + "dev" + normal + "' (completement non-supportées et parfois instables), Une build '" + cyan + "beta" + normal + "' (generalement a jour et suportée a moitiée) ou une build ' " + cyan + "recommandee" + normal + "' (parfois une version majeure en moins ... Mais completement suportée) ? >>>" )
			if version == "recommandee":
				printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
				printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
				urllib.urlretrieve('http://dl.bukkit.org/latest-rb/craftbukkit.jar', './serveur/craftbukkit.jar') # téléchargement de CB (latest - RB)
				ok = True
			elif version == "beta":
				printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
				printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
				urllib.urlretrieve('http://dl.bukkit.org/latest-beta/craftbukkit-beta.jar', './serveur/craftbukkit.jar') # téléchargement de CB (latest - beta)
				ok = True
			elif version == "dev":
				printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
				printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
				urllib.urlretrieve('http://dl.bukkit.org/latest-dev/craftbukkit-dev.jar', './serveur/craftbukkit.jar') # téléchargement de CB (latest - dev)
				ok = True
			else :
				printerror ("Version " + version + " non trouvée ... Choisisez entre recommandee, beta et dev")
	except:
		printerror("Dossier serveur introuvable : lance une installation !")
		installprocess()
###############

def generation(sleep):
	printinfo("Attente de la generation des fichiers")
	subprocess.call(["open", "./serveur/serveur/demarrer.command"]) # Lancement du serveur
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
	printinfo ("Cela peut prendre 1 a 2 minutes ... Veuillez patienter et ne pas aretter le processus")
	urllib.urlretrieve(url, './serveur/serveur/plugins/' + nom + ".zip")
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
	ok = False
	while ok is not True:
		version = raw_input("Quelle version de craft bukkit voulez vous ? Une build de '" + cyan + "dev" + normal + "' (completement non-supportées et parfois instables), Une build '" + cyan + "beta" + normal + "' (generalement a jour et suportée a moitiée) ou une build ' " + cyan + "recommandee" + normal + "' (parfois une version majeure en moins ... Mais completement suportée) ? >>>" )
		if version == "recommandee":
			printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
			printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
			urllib.urlretrieve('http://dl.bukkit.org/latest-rb/craftbukkit.jar', './serveur/serveur/craftbukkit.jar') # téléchargement de CB (latest - RB)
			ok = True
		elif version == "beta":
			printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
			printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
			urllib.urlretrieve('http://dl.bukkit.org/latest-beta/craftbukkit-beta.jar', './serveur/serveur/craftbukkit.jar') # téléchargement de CB (latest - beta)
			ok = True
		elif version == "dev":
			printinfo ("Télechargement de la derniere version " + version + " de craft bukkit")
			printwarn ("Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus")
			urllib.urlretrieve('http://dl.bukkit.org/latest-dev/craftbukkit-dev.jar', './serveur/serveur/craftbukkit.jar') # téléchargement de CB (latest - dev)
			ok = True
		elif version =="pass":
			ok = True
			printwarn ("Aucun telechargement !!!!")
		else :
			printerror("Version " + version + " non trouvée ... Choisisez entre recommandee, beta et dev")
	printinfo ("Lancement du serveur ... Veuillez ne rien toucher !")
	generation(60) # Generation des fichiers par un lancement du serveur


###############

def plugins(lancer):
	## INSTALL ESSENTIALS ##
	dlzip ("essentials","http://ess.ementalo.com/repository/download/bt2/.lastSuccessful/Essentials.zip?guest=1")
	if lancer == True:
		printinfo ("Lancement du serveur pour creer la config essentials !")
		generation(40)
	## INSTALL PEX ##
	dlzip("pex","http://dev.bukkit.org/media/files/659/820/PermissionsEx-1.19.5-package.zip")
	## INSTALL WE ##
	dlzip("we","http://dev.bukkit.org/media/files/698/942/worldedit-5.5.6.zip")
	## INSTALL WG ##
	dlzip("wg","http://dev.bukkit.org/media/files/702/797/worldguard-5.7.4.zip")
	## INSTALL BOSE ECO ##
	dlzip("boseecon","http://dev.bukkit.org/media/files/577/409/BOSEcon0731.zip")
	## INSTALL DYNMAP ##
	dlzip("dynmap","http://webbukkit.org/jenkins/public/dynmap/dynmap-HEAD-bin.zip")
	os.system("rm ./serveur/serveur/plugins/wg/contrib") # Dossier particulier 
	## INSTALL VAULT ##
	dl("vault","http://dev.bukkit.org/media/files/694/78/Vault.jar") 
	## INSTALL NO CHEAT PLUS ##
	dl("ncp","http://ci.md-5.net/job/NoCheatPlus/lastSuccessfulBuild/artifact/target/NoCheatPlus.jar")

###############

def config():
	printinfo ("Genération des dernieres configurations")
	generation(30)
	op = raw_input("Entrez le nom de l'operateur du serveur >>>")
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
	for ligne in proprietees:
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
			slots = raw_input("Indiquez le nombre de slots >>>")
			temp.write("max-players=" + slots)
		elif "motd=" in ligne:
			motd = raw_input("Indiquez le motd >>>")
			temp.write("motd=" + motd)
		else: # Ligne(s) qui ne correspond a rien
			temp.write(ligne + "\n")
	os.system("rm ./serveur/serveur/server.properties")
	os.rename("./serveur/serveur/.server.properties.temp", "./serveur/serveur/server.properties")
	
###############

def finition():
	printinfo ("Génération des derniers fichiers !")
	os.system("rm -R ./serveur/serveur/plugins/Modifyworld.jar")
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

def prop(question,oui,non,defaut):
	temp = open("./serveur/serveur/.server.properties.temp","a")
	reponse = raw_input(question)
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
	
###############

def majPL():
	try:
		os.mkdir("./serveur/serveur")
		os.mkdir("./serveur/serveur/plugins")
	except:
		printerror("Hummm ... Les dossiers sont deja crées ?")
		pass
	plugins(False)
	os.system("mv ./serveur/serveur/plugins/* ./serveur/plugins")
	finition()
	
###############
# 
def tbg(path):
	leaderboard = open(path,"r")
	joueurs = []
	for ligne in leaderboard:
	
		joueurs.append(ligne.replace("\n",""))
	joueurs.sort() # Tout est bien rangé !
	joueurprecedent = ""
	for joueur in joueurs:
		if not joueurprecedent == joueur :
			printinfo(joueur + "a gagné " + str(joueurs.count(joueur)) + " fois")
		joueurprecedent = joueur
############## MAIN ##############

#       #      #      #########  ##    #
##     ##     # #         #      # #   #
# #   # #    #   #        #      #  #  #
#  # #  #   #######       #      #   # #
#   #   #  #       #  #########  #    ##



log = open("./log.txt","a")
printinfo("Loading ...")

chrono = time.time() # Demarrage du chrono
ok = False
while ok is not True:
	start = raw_input("Installation (install) ou statistiques (stats) ou mise a jour de craft bukkit (majCB) ou Mise a jour des plugins (majPL) ou une fonction de stat pour le plugin The bukkitgames (tbg) ? >>>")
	if start == "install":
		ok = True
		installprocess()
	elif start == "stats":
		ok = True
		path = raw_input("Deplacez ici votre fichier server.log et tapez entrer >>>")
		printinfo ("Lancement du processus : cela peut prendre du temps !")
		mclp(path.replace(" ",""))
	elif start == "majCB":
		majCB()
		ok = True
	elif start == "majPL":
		majPL()
		ok = True
 	elif start == "config":
  		config()
  		ok = True
  	elif start == "tbg":
  		path = raw_input("Deplacez ici votre fichier leaderboard et tapez entrer >>>")
		printinfo ("Lancement du processus")
		tbg(path.replace(" ",""))
	else :
		ok = False
		printerror("Soit install, soit stats, soit majCB, soit majPL, soit tbg :)")
log.close()


############################################################

######  ######  #######
#       #    #  #
######  #    #  ####
#       #    #  #
######  ######  #
