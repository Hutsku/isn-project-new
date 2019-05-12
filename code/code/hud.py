import pygame
from pygame.locals import *

import editeur.widget as widget
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

		self.widg_temps = widget.Label((800+22, 227), size=(112,36), color = (0, 0, 0, 0), text = "temps", text_color = (255, 255, 255), centered = True)
		self.widg_score = widget.Label((800+22, 382), size=(112,36), color = (0, 0, 0, 0), text = "score", text_color = (255, 255, 255), centered = True)	
		
	def update(self, temps, score):
		pygame.display.get_surface().blit(self.image, self.rect_hud)
		self.widg_temps.change_text(str(temps))
		self.widg_score.change_text(str(score))
		self.widg_score.update()
		self.widg_temps.update()
		
	def kill(self):
		self.widg_score.kill()
		self.widg_temps.kill()