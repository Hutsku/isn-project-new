import pygame
import config
from pygame.locals import *


import objet

class Dongeon ():
	def __init__(self):
		self.niveau = Niveau("../niveau/test.txt") # on crée un niveau par défaut

	def build(self):
		'''construit les murs et objets d'après les coordonnées du niveau'''
		taille_case = config.getConfig()["taille_case"]
		for mur in self.niveau.coord["mur"]:
			position = (mur[0]*taille_case, mur[1]*taille_case)
			objet.Mur(position, (taille_case, taille_case))
		objet.Escalier((self.niveau.fin[0]*taille_case, self.niveau.fin[1]*taille_case), (taille_case, taille_case)) 
	
	def depart(self):
		taille_case = config.getConfig()["taille_case"]
		taille_personnage = config.getConfig()["taille_personnage"]
		spawn=((self.niveau.spawn[0]*taille_case+taille_personnage, self.niveau.spawn[1]*taille_case)) #ici le +taille_personnage permet d'eviter de spawn dans le mur
		return spawn

	def get_level(self):
		''' renvoit le niveau actuel '''
		return self.niveau

	def change_level(self):
		''' change le niveau du dongeon '''
		print("changement de niveau...")

	def set_level(self, niveau):
		''' change le niveau actuel par celui donnée en argument '''
		if type(niveau) != type(self.niveau):
			print("Vous devez passer un niveau valide en argument.")
		else:
			self.niveau = niveau

class Niveau ():
	def __init__(self, lien):
		self.lien_lvl = lien
		self.spawn = None
		self.fin = None
		self.coord = {"mur": [], "objet": []}
		
		self.build()
		
	def build (self):
		with open(self.lien_lvl, "r") as fichier: #on ouvre le fichier du lien
			caseY=0 #initialisation de la case ligne Y  a 0
			for line in fichier.readlines(): 
				caseX=0 #initialisation de la case ligne X a 0
				for lettre in line:
					if lettre == "D": #Si D (départ)
						self.spawn = (caseX, caseY)
					if lettre == "F": #Si F (fin)
						self.fin = (caseX, caseY)
					if lettre == "x": #Si x (mur)
						self.coord["mur"].append((caseX, caseY))
					caseX +=1
				caseY += 1
	
	def check (self):
		print(("perso:", self.spawn))
		print(("trappe:", self.fin))
		print("mur")
		for mur in self.coord["mur"]:
			print(mur)
	
	
	
	
		#self.coord["mur"].append({"dimension": (50, 200), "position": (100, 100), "type": 1}) # on ajoute un mur à une position et une dimension