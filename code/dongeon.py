import pygame
from pygame.locals import *

import objet
import config

class Dongeon ():
	def __init__(self):
		self.niveau = Niveau("../niveau/test.txt") # on crée un niveau par défaut

		self.taille_case = config.getConfig()["taille_case"]
		self.taille_personnage = config.getConfig()["taille_personnage"]

		self.spawn = self.niveau.spawn

	def build(self):
		'''construit les murs et objets d'après les coordonnées du niveau'''
		for mur in self.niveau.coord["mur"]:
			position = (mur[0]*self.taille_case, mur[1]*self.taille_case)
			objet.Mur(position, (self.taille_case, self.taille_case))

		objet.Escalier((self.niveau.fin[0]*self.taille_case, self.niveau.fin[1]*self.taille_case), (self.taille_case, self.taille_case)) 
	
	# ============================== FONCTION GET =====================================

	def get_spawn(self):
		''' Renvoit la position du spawn du personnage '''
		spawn = (self.spawn[0]*self.taille_case, self.spawn[1]*self.taille_case)
		return spawn

	def get_level(self):
		''' Renvoit le niveau actuel '''
		return self.niveau

	# ================================== PARAMETRE NIVEAU ============================

	def change_level(self, niveau=None):
		''' Change le niveau du dongeon '''

		if niveau: # Si un niveau ets passé en paramètre, on met celui-ci ...
			if type(niveau) != type(self.niveau):
				print("Vous devez passer un niveau valide en argument.")
			else:
				self.niveau = niveau

		else: # ... sinon c'est automatique
			print("changement de niveau...")
		

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