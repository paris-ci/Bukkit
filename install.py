#!/usr/bin/python
# -*- coding: UTF-8 -*-

## AUTO INSTALL PAR ARTHUR ##

############## VARS ##############

VERT="\033[1;32m"
NORMAL="\033[0;39m"
ROUGE="\033[1;31m"
ROSE="\033[1;35m"
BLEU="\033[1;34m"
BLANC="\033[0;02m"
BLANCLAIR="\033[1;08m"
JAUNE="\033[1;33m"
CYAN="\033[1;36m"

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


############### MCLP : https://github.com/stevenleeg/Minecraft-Log-Parser

def mclp(path):
	sauvgarde = open("stats.txt","w")

	actions = {
		"login": re.compile("([0-9]{4})\-([0-9]{2})\-([0-9]{2}) ([0-2][0-9])\:([0-9]{2})\:([0-9]{2}) \[INFO\] ([A-z0-9]*) ?\[\/[0-9.]{4,15}\:[0-9]*\]"),
	    "logout": re.compile("([0-9]{4})\-([0-9]{2})\-([0-9]{2}) ([0-2][0-9])\:([0-9]{2})\:([0-9]{2}) \[INFO\] ([A-z0-9]*) lost connection"),
	    "server_stop": re.compile("([0-9]{4})\-([0-9]{2})\-([0-9]{2}) ([0-2][0-9])\:([0-9]{2})\:([0-9]{2}) \[INFO\] Stopping server")
	}
	f = open(path)
	online = {}
	totals = {}
	for line in f.readlines():
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

	counter = 0
	for time in times:
		counter = counter + 1
		print "%2d) %s" % (counter, time)
		sauvgarde.write("%2d) %s" % (counter, time) + "\n")
		
	f.close()
	sauvgarde.close()

###############


def generation(sleep):
	print (VERT + "Attente de la generation des fichiers" + NORMAL)
	subprocess.call(["open", "./serveur/serveur/demarrer.command"]) # Lancement du serveur
	print (VERT + "Patientez " + str(sleep) + " secondes ..." + NORMAL)
	progressbar(sleep) # Barre de progression
	print (VERT + "Arret du serveur" + NORMAL)
	os.system("killall java") # Quitter java
	print (ROUGE + "Vous pouvez quitter le teminal <serveur> (celui avec [OPERATION TERMINEE] et sans couleurs)" + NORMAL)
	
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
	print (VERT + "Installation de " + nom +" !" + NORMAL)
	print (JAUNE + "Cela peut prendre 1 a 2 minutes ... Veuillez patienter et ne pas aretter le processus" + NORMAL)
	urllib.urlretrieve(url, './serveur/serveur/plugins/' + nom + ".jar") #DL + nom
	print (VERT + "Téléchargement terminé" + NORMAL)
	print (VERT + nom + " installé" + NORMAL)
	
###############

def dlzip(nom,url):
	print (VERT + "Installation de " + nom + " !" + NORMAL)
	print (JAUNE + "Cela peut prendre 1 a 2 minutes ... Veuillez patienter et ne pas aretter le processus" + NORMAL)
	urllib.urlretrieve(url, './serveur/serveur/plugins/' + nom + ".zip")
	print (VERT + "Téléchargement terminé" + NORMAL)
	print (VERT + "Extraction du .zip" + NORMAL)
	with zipfile.ZipFile('./serveur/serveur/plugins/' + nom +'.zip', "r") as z: # Extraction des fichiers indispensables
	    z.extractall("./serveur/serveur/plugins/" + nom)
	print (VERT + nom + " installé" + NORMAL)
	print (VERT + "Effacement de l'archive" + NORMAL)
	os.system("rm ./serveur/serveur/plugins/" + nom + ".zip") # Suppression du zip
	print (VERT + "Effacement terminé" + NORMAL)
	print (VERT + "Deplacement des plugins" + NORMAL) 
	os.system("mv ./serveur/serveur/plugins/" + nom + "/* ./serveur/serveur/plugins") # Sortie du dossier décompressé
	print (VERT + """Suppression du dossier """ + nom + """ inutile""" + NORMAL)
	os.system("rm -R ./serveur/serveur/plugins/" + nom) # Suppression du dossier décompressé vide
	
###############
def install():
	print (VERT + "Instalation automatique de bukkit sous mac" + NORMAL)
	print (VERT + "Preparation ... Appuyez sur entrer pour continuer" + NORMAL)
#	start = raw_input(">>>") # Pour apres passer des arguments au boot si besoin : utiliser la variable start
	print (VERT + "Extraction des fichiers indispensables" + NORMAL)
	with zipfile.ZipFile('serveur.zip', "r") as z: # Extraction des fichiers indispensables
	    z.extractall("serveur")
	print (VERT + "Finition de l'extraction ..." + NORMAL)
	os.system("rm -R ./serveur/__MACOSX") # Suppression d'un dossier inutile
	ok = False
	while ok is not True:
		version = raw_input(JAUNE + "Quelle version de craft bukkit voulez vous ? Une build de '" + CYAN + "dev" + JAUNE + "' (completement non-supportées et parfois instables), Une build '" + CYAN + "beta" + JAUNE + "' (generalement a jour et suportée a moitiée) ou une build ' " + CYAN + "recommandee" + JAUNE + "' (parfois une version majeure en moins ... Mais completement suportée) ? >>>" + NORMAL)
		if version == "recommandee":
			print (VERT + "Télechargement de la derniere version " + version + " de craft bukkit" + NORMAL)
			print (JAUNE + "Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus" + NORMAL)
			urllib.urlretrieve('http://dl.bukkit.org/latest-rb/craftbukkit.jar', './serveur/serveur/craftbukkit.jar') # téléchargement de CB (latest - RB)
			ok = True
		elif version == "beta":
			print (VERT + "Télechargement de la derniere version " + version + " de craft bukkit" + NORMAL)
			print (JAUNE + "Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus" + NORMAL)
			urllib.urlretrieve('http://dl.bukkit.org/latest-beta/craftbukkit-beta.jar', './serveur/serveur/craftbukkit.jar') # téléchargement de CB (latest - beta)
			ok = True
		elif version == "dev":
			print (VERT + "Télechargement de la derniere version " + version + " de craft bukkit" + NORMAL)
			print (JAUNE + "Cela peut prendre 2 a 3 minutes ... Veuillez patienter et ne pas aretter le processus" + NORMAL)
			urllib.urlretrieve('http://dl.bukkit.org/latest-dev/craftbukkit-dev.jar', './serveur/serveur/craftbukkit.jar') # téléchargement de CB (latest - dev)
			ok = True
		else :
			print (ROUGE + "Version " + version + " non trouvée ... Choisisez entre recommandee, beta et dev" + NORMAL)
	print (VERT + "Autorisation de l'executable")
	os.system("chmod +x ./serveur/serveur/demarrer.command") # Rends executable demarrer.command
	print (VERT + "Lancement du serveur ... Veuillez ne rien toucher !" + NORMAL)
	generation(60) # Generation des fichiers par un lancement du serveur

###############

def plugins():
	## INSTALL ESSENTIALS ##
	dlzip ("essentials","http://ess.ementalo.com/repository/download/bt2/.lastSuccessful/Essentials.zip?guest=1")
	print (VERT + "Lancement du serveur pour creer la config essentials !" + NORMAL)
	generation(40)
	## INSTALL PEX ##
	dlzip("pex","http://dev.bukkit.org/media/files/659/820/PermissionsEx-1.19.5-package.zip")
	## INSTALL WE ##
	dlzip("we","http://dev.bukkit.org/media/files/698/942/worldedit-5.5.6.zip")
	## INSTALL WG ##
	dlzip("wg","http://dev.bukkit.org/media/files/702/797/worldguard-5.7.4.zip")
	## INSTALL BOSE ECO ##
	dlzip("boseecon","http://dev.bukkit.org/media/files/577/409/BOSEcon0731.zip")
	dlzip("dynmap","http://webbukkit.org/jenkins/public/dynmap/dynmap-HEAD-bin.zip")
	os.system("rm ./serveur/serveur/plugins/wg/contrib") # Dossier particulier 
	## INSTALL VAULT ##
	dl("vault","http://dev.bukkit.org/media/files/694/78/Vault.jar") 
	## INSTALL NO CHEAT PLUS ##
	dl("ncp","http://dev.bukkit.org/media/files/705/88/NoCheatPlus.jar")

###############

def config():
	print (VERT + "Genération des dernieres configurations" + NORMAL)
	generation(30)
	op = raw_input(BLEU + "Entrez le nom de l'operateur du serveur >>>" + NORMAL)
	sauvgarde = open("./serveur/serveur/ops.txt","a")
	sauvgarde.write(str(op) + "\n")
	sauvgarde.close()
	print (VERT + "Operateur ajouté a la liste des operateurs...")
	sauvgarde = open("./serveur/serveur/white-list.txt","a")
	sauvgarde.write(str(op) + "\n")
	sauvgarde.close()
	print (VERT + "Operateur ajouté a la whitelist" + NORMAL)
###############

def finition():
	print (VERT + "Génération des derniers fichiers !" + NORMAL)
	os.system("rm -R ./serveur/serveur/plugins/Modifyworld.jar")
	generation(60)
	print (JAUNE + "Deplacement des fichiers serveurs ..." + NORMAL)
	os.system("mv ./serveur/serveur/* ./serveur")
	print (VERT + "Supression du dossier temporaire" + NORMAL)
	os.system("rm -R ./serveur/serveur")
	print (VERT + "Suppression des readme" + NORMAL)
	os.system("rm -R ./serveur/plugins/CHANGELOG.txt")
	os.system("rm -R ./serveur/plugins/LICENSE.txt")
	os.system("rm -R ./serveur/plugins/README.html")
	temps = float(time.time()) - float(chrono)
	tempsmin = float(temps)/float(60)
	print (ROSE + "Temps passé sur l'install : " + str(temps) + " secondes soit " + str(tempsmin) + " minute(s)" + NORMAL) # Fin du chrono

############## MAIN ##############

#       #      #      #########  ##    #
##     ##     # #         #      # #   #
# #   # #    #   #        #      #  #  #
#  # #  #   #######       #      #   # #
#   #   #  #       #  #########  #    ##

print("\nLoading ...")
chrono = time.time() # Demarrage du chrono
ok = False
while ok is not True:
	start = raw_input(VERT + "Installation (install) ou statistiques (stats) >>>" + NORMAL)
	if start == "install":
		ok = True
		install()
		print (JAUNE + "Passons a l'installation des plugins ..." + NORMAL)
		plugins()
		print (JAUNE + "Passons a la configuration" + NORMAL)
		config()
		print (JAUNE + "Passons a la finition..." + NORMAL)
		finition()
		print (CYAN + "FIN DE L'INSTALATION !" + NORMAL)
		
	elif start == "stats":
		ok = True
		path = raw_input("Deplacez ici votre fichier server.log et tapez entrer (pensez a enlever l'espace a la fin du path !) >>>")
		mclp(path)
	else :
		ok = False
		print(ROUGE + "Soit install, soit stats :)")



######  ######  #######
#       #    #  #
######  #    #  ####
#       #    #  #
######  ######  #
