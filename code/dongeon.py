import pygame
from pygame.locals import *
import os
import random

import objet
import config

def check_fin_niveau(dongeon_actuel):
	for escalier in objet.Escalier.liste:
		if escalier.statut:
			dongeon_actuel.change_level()

class Dongeon ():
	def __init__(self):
		self.lien_dossier = "../niveau/"
		self.niveau = None # aucun niveau par défaut
		self.change_level() # Choisi un niveau aléatoirement

	def build(self):
		'''construit les murs et objets d'après les coordonnées du niveau'''
		taille_case = config.getConfig()["taille_case"]
		spawn = (self.niveau.spawn[0]*taille_case, self.niveau.spawn[1]*taille_case)
		fin = (self.niveau.fin[0]*taille_case, self.niveau.fin[1]*taille_case)
		
		for mur in self.niveau.coord["mur"]:
			position = (mur[0]*taille_case, mur[1]*taille_case)
			objet.Mur(position, (taille_case, taille_case))

		objet.Escalier(fin, (taille_case, taille_case))

		for perso in objet.Personnage.liste: # On selectionne le personnage (il est censé n'y en avoir que 1)
			perso.move(spawn) # et on le bouge au spawn
	
	def effacer(self):
		''' Détruit tout les objets présent sur le niveau '''
		objet.Mur.liste.empty() # On vide la liste de mur, empechant de les mettre à jour (c'est comme si ils n'existaient plus)
		objet.Sol.liste.empty() # Idem pour les sols.
		objet.Escalier.liste.empty() # Idem pour la fin.

	# ============================== FONCTION GET =====================================

	def get_spawn(self):
		''' Renvoit la position du spawn du personnage '''
		taille_case = config.getConfig()["taille_case"]
		return (self.niveau.spawn[0]*taille_case, self.niveau.spawn[1]*taille_case)

	def get_level(self):
		''' Renvoit le niveau actuel '''
		return self.niveau

	# ================================== PARAMETRE NIVEAU ============================

	def change_level(self, lien_niveau=""):
		''' Change le niveau du dongeon '''
		meme_niveau = True
		while meme_niveau == True:
			if lien_niveau: # Si un niveau est passé en paramètre, on met celui-ci ...
				self.niveau = Niveau(lien_niveau)

			else: # ... sinon c'est automatique
				(path, dirs, filenames) = next(os.walk(self.lien_dossier)) # liste tout les niveaux présent ...
				fichier = random.choice(filenames)
				self.niveau = Niveau(self.lien_dossier+fichier)	# ... puis on en choisit un et on créer le niveau.
				niveau_actuel = self.get_level
				if niveau_actuel == fichier:
					meme_niveau = True
				else:
					meme_niveau = False
		self.effacer() # Puis on efface le précedant ...
		self.build() # ... et on construit le nouveau.

class Niveau ():
	def __init__(self, lien):
		self.lien_lvl = lien
		self.spawn = None
		self.fin = None
		self.coord = {"mur": [], "objet": []}
		
		self.build()
		
	def build (self):
		with open(self.lien_lvl, "r") as fichier: # on ouvre le fichier du lien
			caseY=0 # initialisation de la case ligne Y  a 0
			for line in fichier.readlines(): 
				caseX=0 # initialisation de la case ligne X a 0
				for lettre in line:
					if lettre == "D": # (départ)
						self.spawn = (caseX, caseY)
					if lettre == "F": # (fin)
						self.fin = (caseX, caseY)
					if lettre == "x": # (mur)
						self.coord["mur"].append((caseX, caseY))
					caseX +=1
				caseY += 1
	

	