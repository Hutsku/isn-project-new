import pygame
from pygame.locals import *

import objet

class Dongeon ():
	def __init__(self):
		self.niveau = Niveau((100, 50), (400, 400)) # on crée un niveau par défaut

	def build(self):
		''' construit les murs et objets d'après les coordonnées du niveau'''
		for mur in self.niveau.coord["mur"]:
			objet.Mur(mur["position"], mur["dimension"])

		objet.Escalier((self.niveau.fin), (70, 70))

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
	def __init__(self, spawn, fin):
		self.spawn = spawn
		self.fin = fin
		self.coord = {"mur": [], "objet": []}
		
		self.build()
		
	def build (self):
		self.coord["mur"].append({"dimension": (50, 200), "position": (100, 100), "type": 1}) # on ajoute un mur à une position et une dimension