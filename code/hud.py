import pygame
from pygame.locals import *

import config
# ========================================= INITIALISATION =======================================
config_info = config.getConfig()
config_image = config.getImage()	
# ================================================================================================
		
class Hud():
	def __init__(self):		
		self.dimension = (config_info["taille_HUD"], config_info["taille_level"])
		self.largeur = config_info["taille_HUD"]
		self.position = (config_info["taille_level"], 0)

		self.image = pygame.image.load("../image/hud.png").convert()
		self.image = pygame.transform.scale(self.image, self.dimension)
		
		self.rect_hud = self.image.get_rect()
		self.rect_hud.topleft = (config_info["taille_level"], 0)

		taille_texte = 36
		police = pygame.font.SysFont("Arial", taille_texte, True) 
		
		
	def affichage(self, temps):
		print(temps)
	
	def update(self):
		pygame.display.get_surface().blit(self.image, self.rect_hud)
