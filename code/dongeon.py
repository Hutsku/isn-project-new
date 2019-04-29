import pygame
from pygame.locals import *
import os
import random
import pygame
from pygame.locals import *
import os
import random
import json

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

		x=0
		for a in self.niveau.coord["terrain"]:
			y=0
			for case in self.niveau.coord["terrain"][x]:
				position = (x*taille_case, y*taille_case)
				type_case = case["type"]
				if type_case == "mur":
					objet.Mur(position, (taille_case, taille_case))
				if type_case == "sol":
					objet.Sol(position, (taille_case, taille_case))
				if type_case == "fin":
					objet.Escalier(position, (taille_case, taille_case))
					self.niveau.fin = (x, y)
				y += 1
			x += 1

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
		if lien_niveau: # Si un niveau est passé en paramètre, on met celui-ci ...
			self.niveau = Niveau(lien_niveau)

		else: # ... sinon c'est automatique
			(path, dirs, filenames) = next(os.walk(self.lien_dossier)) # liste tout les niveaux présent ...
			
			if self.niveau: # si il y a déjà un niveau avant ...
				niveau_actuel = self.niveau.lien_lvl.split("/")[-1] # on recupère le nom du level et on l'arrange
				filenames.remove(niveau_actuel) # on enlève de la liste le niveau actuel

			fichier = random.choice(filenames)
			self.niveau = Niveau(self.lien_dossier+fichier)	# ... puis on en choisit un et on créer le niveau.		
				
		self.effacer() # Puis on efface le précedant ...
		self.build() # ... et on construit le nouveau.

class Niveau ():
	def __init__(self, lien):
		self.lien_lvl = lien
		self.spawn = None
		self.coord = {"terrain": [], "objets": []}
		
		self.build()
		
	def build (self):
		with open(self.lien_lvl, "r") as fichier: # on ouvre le fichier du lien
			json_dic = fichier.read()
			dic = json.loads(json_dic)

			self.spawn = dic["spawn"]
			self.coord["terrain"] = dic["terrain"]
			self.coord["objets"] = dic["objets"]
	

	