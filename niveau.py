import pygame
from pygame.locals import *

import classe

class Niveau ():
	def __init__(self, spawn, fin, murs = [], objets = []):
		self.spawn = spawn
		self.fin = fin
		self.murs = murs
		self.objets = objets
		
		self.generer()
		
	def generer (self):
		#mur = classe.Mur((), (50, 1000))
		escalier = classe.Escalier((self.fin), (70, 70))